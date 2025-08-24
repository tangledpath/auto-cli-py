# Auto-generate CLI from function signatures and docstrings.
import argparse
import enum
import inspect
import sys
import traceback
import types
from collections.abc import Callable
from typing import Any, Optional, Type, Union


from .command_executor import CommandExecutor
from .command_builder import CommandBuilder
from .docstring_parser import extract_function_help, parse_docstring
from .formatter import HierarchicalHelpFormatter

Target = Union[types.ModuleType, Type[Any]]


class TargetMode(enum.Enum):
  """Target mode enum for CLI generation."""
  MODULE = 'module'
  CLASS = 'class'


class CLI:
  """Automatically generates CLI from module functions or class methods using introspection."""

  def __init__(self, target: Target, title: Optional[str] = None, function_filter: Optional[Callable] = None,
               method_filter: Optional[Callable] = None, theme=None, alphabetize: bool = True, 
               enable_completion: bool = False):
    """Initialize CLI generator with auto-detection of target type.

    :param target: Module or class containing functions/methods to generate CLI from
    :param title: CLI application title (auto-generated from class docstring if None for classes)
    :param function_filter: Optional filter function for selecting functions (module mode)
    :param method_filter: Optional filter function for selecting methods (class mode)
    :param theme: Optional theme for colored output
    :param alphabetize: If True, sort commands and options alphabetically
    :param enable_completion: Enable shell completion support
    """
    # Auto-detect target type
    if inspect.isclass(target):
      self.target_mode = TargetMode.CLASS
      self.target_class = target
      self.target_module = None
      self.title = title or self.__extract_class_title(target)
      self.method_filter = method_filter or self.__default_method_filter
      self.function_filter = None
    elif inspect.ismodule(target):
      self.target_mode = TargetMode.MODULE
      self.target_module = target
      self.target_class = None
      self.title = title or "CLI Application"
      self.function_filter = function_filter or self.__default_function_filter
      self.method_filter = None
    else:
      raise ValueError(f"Target must be a module or class, got {type(target).__name__}")

    self.theme = theme
    self.alphabetize = alphabetize
    self.enable_completion = enable_completion

    # Discover functions/methods based on target mode
    if self.target_mode == TargetMode.MODULE:
      self.__discover_functions()
    else:
      self.__discover_methods()

    # Initialize command executor after metadata is set up
    self.command_executor = CommandExecutor(
        target_class=self.target_class,
        target_module=self.target_module,
        inner_class_metadata=getattr(self, 'inner_class_metadata', {})
    )

  def display(self):
    """Legacy method for backward compatibility - runs the CLI."""
    self.run()

  def run(self, args: list | None = None) -> Any:
    """Parse arguments and execute the appropriate function."""
    # Check for completion requests early
    if self.enable_completion and self._is_completion_request():
      self._handle_completion()

    # First, do a preliminary parse to check for --no-color flag
    # This allows us to disable colors before any help output is generated
    no_color = False
    if args:
      no_color = '--no-color' in args or '-n' in args

    parser = self.create_parser(no_color=no_color)
    parsed = None

    try:
      parsed = parser.parse_args(args)

      # Handle missing command scenarios
      if not hasattr(parsed, '_cli_function'):
        # argparse has already handled validation, just show appropriate help
        if hasattr(parsed, 'command') and parsed.command:
          # User specified a valid group command, find and show its help
          for action in parser._actions:
            if isinstance(action, argparse._SubParsersAction) and parsed.command in action.choices:
              action.choices[parsed.command].print_help()
              return 0
        
        # No command or unknown command, show main help  
        parser.print_help()
        return 0
      else:
        # Execute the command using CommandExecutor
        return self.command_executor.execute_command(
            parsed, 
            self.target_mode, 
            getattr(self, 'use_inner_class_pattern', False),
            getattr(self, 'inner_class_metadata', {})
        )

    except SystemExit:
      # Let argparse handle its own exits (help, errors, etc.)
      raise
    except Exception as e:
      # Handle execution errors gracefully
      if parsed is not None:
        return self.command_executor.handle_execution_error(parsed, e)
      else:
        # If parsing failed, this is likely an argparse error - re-raise as SystemExit
        raise SystemExit(1)

  def __extract_class_title(self, cls: type) -> str:
    """Extract title from class docstring, similar to function docstring extraction."""
    if cls.__doc__:
      main_desc, _ = parse_docstring(cls.__doc__)
      return main_desc or cls.__name__
    return cls.__name__

  def __default_function_filter(self, name: str, obj: Any) -> bool:
    """Default filter: include non-private callable functions defined in this module."""
    return (
        not name.startswith('_') and
        callable(obj) and
        not inspect.isclass(obj) and
        inspect.isfunction(obj) and
        obj.__module__ == self.target_module.__name__  # Exclude imported functions
    )

  def __default_method_filter(self, name: str, obj: Any) -> bool:
    """Default filter: include non-private callable methods defined in target class."""
    return (
        not name.startswith('_') and
        callable(obj) and
        (inspect.isfunction(obj) or inspect.ismethod(obj)) and
        hasattr(obj, '__qualname__') and
        self.target_class.__name__ in obj.__qualname__  # Check if class name is in qualname
    )

  def __discover_functions(self):
    """Auto-discover functions from module using the filter."""
    self.functions = {}
    for name, obj in inspect.getmembers(self.target_module):
      if self.function_filter(name, obj):
        self.functions[name] = obj

    # Build hierarchical command structure using CommandBuilder
    self.commands = self._build_commands()

  def __discover_methods(self):
    """Auto-discover methods from class using inner class pattern or direct methods."""
    self.functions = {}

    # Check for inner classes first (hierarchical organization)
    inner_classes = self.__discover_inner_classes()

    if inner_classes:
      # Use mixed pattern: both direct methods AND inner class methods
      # Validate main class and inner class constructors
      self.__validate_constructor_parameters(self.target_class, "main class")
      for class_name, inner_class in inner_classes.items():
        self.__validate_inner_class_constructor_parameters(inner_class, f"inner class '{class_name}'")

      # Discover both direct methods and inner class methods
      self.__discover_direct_methods()  # Direct methods on main class
      self.__discover_methods_from_inner_classes(inner_classes)  # Inner class methods
      self.use_inner_class_pattern = True
    else:
      # Use direct methods from the class (flat commands only)
      # For direct methods, class should have parameterless constructor or all params with defaults
      self.__validate_constructor_parameters(self.target_class, "class", allow_parameterless_only=True)

      self.__discover_direct_methods()
      self.use_inner_class_pattern = False

    # Build hierarchical command structure using CommandBuilder
    self.commands = self._build_commands()

  def __discover_inner_classes(self) -> dict[str, type]:
    """Discover inner classes that should be treated as command groups."""
    inner_classes = {}

    for name, obj in inspect.getmembers(self.target_class):
      if (inspect.isclass(obj) and
          not name.startswith('_') and
          obj.__qualname__.endswith(f'{self.target_class.__name__}.{name}')):
        inner_classes[name] = obj

    return inner_classes

  def __validate_constructor_parameters(self, cls: type, context: str, allow_parameterless_only: bool = False):
    """Validate constructor parameters using ValidationService."""
    from .validation import ValidationService
    ValidationService.validate_constructor_parameters(cls, context, allow_parameterless_only)

  def __validate_inner_class_constructor_parameters(self, cls: type, context: str):
    """Validate inner class constructor parameters - first parameter should be main_instance."""
    from .validation import ValidationService
    ValidationService.validate_inner_class_constructor_parameters(cls, context)

  def __discover_methods_from_inner_classes(self, inner_classes: dict[str, type]):
    """Discover methods from inner classes for the new pattern."""
    from .str_utils import StrUtils

    # Store inner class info for later use in parsing/execution
    self.inner_classes = inner_classes
    self.use_inner_class_pattern = True

    # For each inner class, discover its methods
    for class_name, inner_class in inner_classes.items():
      command_name = StrUtils.kebab_case(class_name)

      # Get methods from the inner class
      for method_name, method_obj in inspect.getmembers(inner_class):
        if (not method_name.startswith('_') and
            callable(method_obj) and
            method_name != '__init__' and
            inspect.isfunction(method_obj)):

          # Create hierarchical name: command__command
          hierarchical_name = f"{command_name}__{method_name}"
          self.functions[hierarchical_name] = method_obj

          # Store metadata for execution
          if not hasattr(self, 'inner_class_metadata'):
            self.inner_class_metadata = {}
          self.inner_class_metadata[hierarchical_name] = {
            'inner_class': inner_class,
            'inner_class_name': class_name,
            'command_name': command_name,
            'method_name': method_name
          }

  def __discover_direct_methods(self):
    """Discover methods directly from the class (flat command structure)."""
    # Get all methods from the class that match our filter
    for name, obj in inspect.getmembers(self.target_class):
      if self.method_filter(name, obj):
        # Store the unbound method - it will be bound at execution time
        self.functions[name] = obj

  def _init_completion(self, shell: str = None):
    """Initialize completion handler if enabled.

    :param shell: Target shell (auto-detect if None)
    """
    if not self.enable_completion:
      return

    try:
      from .completion import get_completion_handler
      self._completion_handler = get_completion_handler(self, shell)
    except ImportError:
      # Completion module not available
      self.enable_completion = False

  def _is_completion_request(self) -> bool:
    """Check if this is a completion request."""
    import os
    return os.getenv('_AUTO_CLI_COMPLETE') is not None

  def _handle_completion(self):
    """Handle shell completion request."""
    if hasattr(self, '_completion_handler'):
      self._completion_handler.complete()
    else:
      # Initialize completion handler and try again
      self._init_completion()
      if hasattr(self, '_completion_handler'):
        self._completion_handler.complete()





  def _build_commands(self) -> dict[str, dict]:
    """Build commands using centralized CommandBuilder service."""
    builder = CommandBuilder(
        target_mode=self.target_mode,
        functions=self.functions,
        inner_classes=getattr(self, 'inner_classes', {}),
        use_inner_class_pattern=getattr(self, 'use_inner_class_pattern', False)
    )
    return builder.build_command_tree()


  def create_parser(self, no_color: bool = False) -> argparse.ArgumentParser:
    """Create argument parser with hierarchical command group support."""
    # Create a custom formatter class that includes the theme (or no theme if no_color)
    effective_theme = None if no_color else self.theme

    def create_formatter_with_theme(*args, **kwargs):
      formatter = HierarchicalHelpFormatter(*args, theme=effective_theme, alphabetize=self.alphabetize, **kwargs)
      return formatter

    parser = argparse.ArgumentParser(
      description=self.title,
      formatter_class=create_formatter_with_theme
    )

    # Store reference to parser in the formatter class so it can access all actions
    # We'll do this after the parser is fully configured
    def patch_formatter_with_parser_actions():
      original_get_formatter = parser._get_formatter

      def patched_get_formatter():
        formatter = original_get_formatter()
        # Give the formatter access to the parser's actions
        formatter._parser_actions = parser._actions
        return formatter

      parser._get_formatter = patched_get_formatter

    # We need to patch this after the parser is fully set up
    # Store the patch function for later use

    # Monkey-patch the parser to style the title
    original_format_help = parser.format_help

    def patched_format_help():
      # Get original help
      original_help = original_format_help()

      # Apply title styling if we have a theme
      if effective_theme and self.title in original_help:
        from .theme import ColorFormatter
        color_formatter = ColorFormatter()
        styled_title = color_formatter.apply_style(self.title, effective_theme.title)
        # Replace the plain title with the styled version
        original_help = original_help.replace(self.title, styled_title)

      return original_help

    parser.format_help = patched_format_help

    # Add verbose flag for module-based CLIs (class-based CLIs use it as global parameter)
    if self.target_mode == TargetMode.MODULE:
      parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
      )

    # Add global no-color flag
    parser.add_argument(
      "-n", "--no-color",
      action="store_true",
      help="Disable colored output"
    )

    # Add completion-related hidden arguments
    if self.enable_completion:
      parser.add_argument(
        "--_complete",
        action="store_true",
        help=argparse.SUPPRESS  # Hide from help
      )

    # Add global arguments from main class constructor (for inner class pattern)
    if (self.target_mode == TargetMode.CLASS and
        hasattr(self, 'use_inner_class_pattern') and
        self.use_inner_class_pattern):
      from .argument_parser import ArgumentParserService
      ArgumentParserService.add_global_class_args(parser, self.target_class)

    # Main subparsers
    subparsers = parser.add_subparsers(
      title='COMMANDS',
      dest='command',
      required=False,  # Allow no command to show help
      help='Available commands',
      metavar=''  # Remove the comma-separated list
    )

    # Store theme reference for consistency in subparsers
    subparsers._theme = effective_theme

    # Add commands (flat, groups, and nested groups)
    self.__add_commands_to_parser(subparsers, self.commands, [])

    # Now that the parser is fully configured, patch the formatter to have access to actions
    patch_formatter_with_parser_actions()

    return parser

  def __add_commands_to_parser(self, subparsers, commands: dict, path: list):
    """Recursively add commands to parser, supporting arbitrary nesting."""
    for name, info in commands.items():
      if info['type'] == 'group':
        self.__add_command_group(subparsers, name, info, path + [name])
      elif info['type'] == 'command':
        self.__add_leaf_command(subparsers, name, info)

  def __add_command_group(self, subparsers, name: str, info: dict, path: list):
    """Add a command group with commands (supports nesting)."""
    # Check for inner class description
    group_help = None
    inner_class = None

    if 'description' in info:
      group_help = info['description']
    else:
      group_help = f"{name.title().replace('-', ' ')} operations"

    # Find the inner class for this command group (for sub-global arguments)
    # First check if it's provided directly in the info (for system commands)
    if 'inner_class' in info and info['inner_class']:
      inner_class = info['inner_class']
    elif (hasattr(self, 'use_inner_class_pattern') and
          self.use_inner_class_pattern and
          hasattr(self, 'inner_classes')):
      for class_name, cls in self.inner_classes.items():
        from .str_utils import StrUtils
        if StrUtils.kebab_case(class_name) == name:
          inner_class = cls
          break

    # Get the formatter class from the parent parser to ensure consistency
    effective_theme = getattr(subparsers, '_theme', self.theme)

    def create_formatter_with_theme(*args, **kwargs):
      return HierarchicalHelpFormatter(*args, theme=effective_theme, alphabetize=self.alphabetize, **kwargs)

    group_parser = subparsers.add_parser(
      name,
      help=group_help,
      formatter_class=create_formatter_with_theme
    )

    # Add sub-global arguments from inner class constructor
    if inner_class:
      from .argument_parser import ArgumentParserService
      ArgumentParserService.add_subglobal_class_args(group_parser, inner_class, name)

    # Store description for formatter to use
    if 'description' in info:
      group_parser._command_group_description = info['description']
    group_parser._command_type = 'group'

    # Mark as System command if applicable
    if 'is_system_command' in info:
      group_parser._is_system_command = info['is_system_command']

    # Store theme reference for consistency
    group_parser._theme = effective_theme

    # Store command info for help formatting
    command_help = {}
    for cmd_name, cmd_info in info['commands'].items():
      if cmd_info['type'] == 'command':
        func = cmd_info['function']
        desc, _ = extract_function_help(func)
        command_help[cmd_name] = desc
      elif cmd_info['type'] == 'group':
        # For nested groups, use their actual description if available
        if 'description' in cmd_info and cmd_info['description']:
          command_help[cmd_name] = cmd_info['description']
        else:
          command_help[cmd_name] = f"{cmd_name.title().replace('-', ' ')} operations"

    group_parser._commands = command_help
    group_parser._command_details = info['commands']

    # Create command parsers with enhanced help
    # Always use a unique dest name for nested subparsers to avoid conflicts
    dest_name = '_'.join(path) + '_command'
    sub_subparsers = group_parser.add_subparsers(
      title=f'{name.title().replace("-", " ")} COMMANDS',
      dest=dest_name,
      required=False,
      help=f'Available {name} commands',
      metavar=''
    )

    # Store reference for enhanced help formatting
    sub_subparsers._enhanced_help = True
    sub_subparsers._command_details = info['commands']

    # Store theme reference for consistency in nested subparsers
    sub_subparsers._theme = effective_theme

    # Recursively add commands
    self.__add_commands_to_parser(sub_subparsers, info['commands'], path)

  def __add_leaf_command(self, subparsers, name: str, info: dict):
    """Add a leaf command (actual executable function)."""
    func = info['function']
    desc, _ = extract_function_help(func)

    # Get the formatter class from the parent parser to ensure consistency
    effective_theme = getattr(subparsers, '_theme', self.theme)

    def create_formatter_with_theme(*args, **kwargs):
      return HierarchicalHelpFormatter(*args, theme=effective_theme, alphabetize=self.alphabetize, **kwargs)

    sub = subparsers.add_parser(
      name,
      help=desc,
      description=desc,
      formatter_class=create_formatter_with_theme
    )
    sub._command_type = 'command'

    # Store theme reference for consistency
    sub._theme = effective_theme

    from .argument_parser import ArgumentParserService
    ArgumentParserService.add_function_args(sub, func)

    # Set defaults - command_path is optional for direct methods
    defaults = {
      '_cli_function': func,
      '_function_name': info['original_name']
    }

    if 'command_path' in info:
      defaults['_command_path'] = info['command_path']

    if 'is_system_command' in info:
      defaults['_is_system_command'] = info['is_system_command']

    sub.set_defaults(**defaults)




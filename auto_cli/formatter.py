# Auto-generate CLI from function signatures and docstrings - Help Formatter
import argparse
import os
import textwrap

from .formatting_engine import FormattingEngine


class HierarchicalHelpFormatter(argparse.RawDescriptionHelpFormatter):
  """Custom formatter providing clean hierarchical command display."""

  def __init__(self, *args, theme=None, alphabetize=True, **kwargs):
    super().__init__(*args, **kwargs)
    try:
      self._console_width = os.get_terminal_size().columns
    except (OSError, ValueError):
      # Fallback for non-TTY environments (pipes, redirects, etc.)
      self._console_width = int(os.environ.get('COLUMNS', 80))
    self._cmd_indent = 2  # Base indentation for commands
    self._arg_indent = 4  # Indentation for arguments (reduced from 6 to 4)
    self._desc_indent = 8  # Indentation for descriptions
    
    # Initialize formatting engine
    self._formatting_engine = FormattingEngine(
        console_width=self._console_width,
        theme=theme,
        color_formatter=getattr(self, '_color_formatter', None)
    )

    # Theme support
    self._theme = theme
    if theme:
      from .theme import ColorFormatter
      self._color_formatter = ColorFormatter()
    else:
      self._color_formatter = None

    # Alphabetization control
    self._alphabetize = alphabetize

    # Cache for global column calculation
    self._global_desc_column = None

  def _format_actions(self, actions):
    """Override to capture parser actions for unified column calculation."""
    # Store actions for unified column calculation
    self._parser_actions = actions
    return super()._format_actions(actions)

  def _format_action(self, action):
    """Format actions with proper indentation for command groups."""
    result = None
    
    if isinstance(action, argparse._SubParsersAction):
      result = self._format_command_groups(action)
    elif action.option_strings and not isinstance(action, argparse._SubParsersAction):
      # Handle global options with fixed alignment
      result = self._format_global_option_aligned(action)
    else:
      result = super()._format_action(action)
    
    return result

  def _ensure_global_column_calculated(self):
    """Calculate and cache the unified description column if not already done."""
    if self._global_desc_column is not None:
      return self._global_desc_column

    # Find subparsers action from parser actions that were passed to the formatter
    subparsers_action = None
    parser_actions = getattr(self, '_parser_actions', [])

    # Find subparsers action from parser actions
    for act in parser_actions:
      if isinstance(act, argparse._SubParsersAction):
        subparsers_action = act
        break

    if subparsers_action:
      # Use the unified command description column for consistency - this already includes all options
      self._global_desc_column = self._calculate_unified_command_description_column(subparsers_action)
    else:
      # Fallback: Use a reasonable default
      self._global_desc_column = 40

    return self._global_desc_column

  def _format_global_option_aligned(self, action):
    """Format global options with consistent alignment using existing alignment logic."""
    # Build option string
    option_strings = action.option_strings
    result = None
    
    if not option_strings:
      result = super()._format_action(action)
    else:
      # Get option name (prefer long form)
      option_name = option_strings[-1] if option_strings else ""

      # Add metavar if present
      if action.nargs != 0:
        if hasattr(action, 'metavar') and action.metavar:
          option_display = f"{option_name} {action.metavar}"
        elif hasattr(action, 'choices') and action.choices:
          # For choices, show them in help text, not in option name
          option_display = option_name
        else:
          # Generate metavar from dest
          metavar = action.dest.upper().replace('_', '-')
          option_display = f"{option_name} {metavar}"
      else:
        option_display = option_name

      # Prepare help text
      help_text = action.help or ""
      if hasattr(action, 'choices') and action.choices and action.nargs != 0:
        # Add choices info to help text
        choices_str = ", ".join(str(c) for c in action.choices)
        help_text = f"{help_text} (choices: {choices_str})"

      # Get the cached global description column
      global_desc_column = self._ensure_global_column_calculated()

      # Use the existing _format_inline_description method for proper alignment and wrapping
      formatted_lines = self._format_inline_description(
        name=option_display,
        description=help_text,
        name_indent=self._arg_indent + 2,  # Global options indented +2 more spaces (entire line)
        description_column=global_desc_column + 4,  # Global option descriptions +4 spaces (2 for line indent + 2 for desc)
        style_name='option_name',  # Use option_name style (will be handled by CLI theme)
        style_description='option_description',  # Use option_description style
        add_colon=False  # Options don't have colons
      )

      # Join lines and add newline at end
      result = '\n'.join(formatted_lines) + '\n'
    
    return result

  def _calculate_global_option_column(self, action):
    """Calculate global option description column based on longest option across ALL commands."""
    max_opt_width = self._arg_indent

    # Scan all flat commands
    for choice, subparser in action.choices.items():
      if not hasattr(subparser, '_command_type') or subparser._command_type != 'group':
        _, optional_args = self._analyze_arguments(subparser)
        for arg_name, _ in optional_args:
          opt_width = len(arg_name) + self._arg_indent
          max_opt_width = max(max_opt_width, opt_width)

    # Scan all group command groups
    for choice, subparser in action.choices.items():
      if hasattr(subparser, '_command_type') and subparser._command_type == 'group':
        if hasattr(subparser, '_commands'):
          for cmd_name in subparser._commands.keys():
            cmd_parser = self._find_subparser(subparser, cmd_name)
            if cmd_parser:
              _, optional_args = self._analyze_arguments(cmd_parser)
              for arg_name, _ in optional_args:
                opt_width = len(arg_name) + self._arg_indent
                max_opt_width = max(max_opt_width, opt_width)

    # Calculate global description column with padding
    global_opt_desc_column = max_opt_width + 4  # 4 spaces padding

    # Ensure we don't exceed terminal width (leave room for descriptions)
    return min(global_opt_desc_column, self._console_width // 2)

  def _calculate_unified_command_description_column(self, action):
    """Calculate unified description column for ALL elements (global options, commands, command groups, AND options)."""
    max_width = self._cmd_indent

    # Include global options in the calculation
    parser_actions = getattr(self, '_parser_actions', [])
    for act in parser_actions:
      if act.option_strings and act.dest != 'help' and not isinstance(act, argparse._SubParsersAction):
        opt_name = act.option_strings[-1]
        if act.nargs != 0 and getattr(act, 'metavar', None):
          opt_display = f"{opt_name} {act.metavar}"
        elif act.nargs != 0:
          opt_metavar = act.dest.upper().replace('_', '-')
          opt_display = f"{opt_name} {opt_metavar}"
        else:
          opt_display = opt_name
        # Global options use standard arg indentation
        global_opt_width = len(opt_display) + self._arg_indent
        max_width = max(max_width, global_opt_width)

    # Scan all flat commands and their options
    for choice, subparser in action.choices.items():
      if not hasattr(subparser, '_command_type') or subparser._command_type != 'group':
        # Calculate command width: indent + name + colon
        cmd_width = self._cmd_indent + len(choice) + 1  # +1 for colon
        max_width = max(max_width, cmd_width)

        # Also check option widths in flat commands
        _, optional_args = self._analyze_arguments(subparser)
        for arg_name, _ in optional_args:
          opt_width = len(arg_name) + self._arg_indent
          max_width = max(max_width, opt_width)

    # Scan all group commands and their command groups/options
    for choice, subparser in action.choices.items():
      if hasattr(subparser, '_command_type') and subparser._command_type == 'group':
        # Calculate group command width: indent + name + colon
        cmd_width = self._cmd_indent + len(choice) + 1  # +1 for colon
        max_width = max(max_width, cmd_width)

        # Check group-level options
        _, optional_args = self._analyze_arguments(subparser)
        for arg_name, _ in optional_args:
          opt_width = len(arg_name) + self._arg_indent
          max_width = max(max_width, opt_width)

        # Also check command groups within groups
        if hasattr(subparser, '_commands'):
          command_indent = self._cmd_indent + 2
          for cmd_name in subparser._commands.keys():
            # Calculate command width: command_indent + name + colon
            cmd_width = command_indent + len(cmd_name) + 1  # +1 for colon
            max_width = max(max_width, cmd_width)

            # Also check option widths in command groups
            cmd_parser = self._find_subparser(subparser, cmd_name)
            if cmd_parser:
              _, optional_args = self._analyze_arguments(cmd_parser)
              for arg_name, _ in optional_args:
                opt_width = len(arg_name) + self._arg_indent
                max_width = max(max_width, opt_width)

    # Add padding for description (4 spaces minimum)
    unified_desc_column = max_width + 4

    # Ensure we don't exceed terminal width (leave room for descriptions)
    return min(unified_desc_column, self._console_width // 2)

  def _format_command_groups(self, action):
    """Format command groups (sub-commands) with clean list-based display."""
    parts = []
    system_groups = {}
    regular_groups = {}
    flat_commands = {}
    has_required_args = False

    # Calculate unified command description column for consistent alignment across ALL command types
    unified_cmd_desc_column = self._calculate_unified_command_description_column(action)

    # Calculate global option column for consistent alignment across all commands
    global_option_column = self._calculate_global_option_column(action)

    # Separate System groups, regular groups, and flat commands
    for choice, subparser in action.choices.items():
      if hasattr(subparser, '_command_type'):
        if subparser._command_type == 'group':
          # Check if this is a System command group
          if hasattr(subparser, '_is_system_command') and getattr(subparser, '_is_system_command', False):
            system_groups[choice] = subparser
          else:
            regular_groups[choice] = subparser
        else:
          flat_commands[choice] = subparser
      else:
        flat_commands[choice] = subparser

    # Add System groups first (they appear at the top)
    if system_groups:
      system_items = sorted(system_groups.items()) if self._alphabetize else list(system_groups.items())
      for choice, subparser in system_items:
        group_section = self._format_group_with_command_groups_global(
          choice, subparser, self._cmd_indent, unified_cmd_desc_column, global_option_column
        )
        parts.extend(group_section)
        # Check command groups for required args too
        if hasattr(subparser, '_command_details'):
          for cmd_info in subparser._command_details.values():
            if cmd_info.get('type') == 'command' and 'function' in cmd_info:
              # This is a bit tricky - we'd need to check the function signature
              # For now, assume nested commands might have required args
              has_required_args = True

    # Add flat commands with unified command description column alignment
    flat_items = sorted(flat_commands.items()) if self._alphabetize else list(flat_commands.items())
    for choice, subparser in flat_items:
      command_section = self._format_command_with_args_global(choice, subparser, self._cmd_indent,
                                                              unified_cmd_desc_column, global_option_column)
      parts.extend(command_section)
      # Check if this command has required args
      required_args, _ = self._analyze_arguments(subparser)
      if required_args:
        has_required_args = True

    # Add regular groups with their command groups
    if regular_groups:
      if flat_commands or system_groups:
        parts.append("")  # Empty line separator

      regular_items = sorted(regular_groups.items()) if self._alphabetize else list(regular_groups.items())
      for choice, subparser in regular_items:
        group_section = self._format_group_with_command_groups_global(
          choice, subparser, self._cmd_indent, unified_cmd_desc_column, global_option_column
        )
        parts.extend(group_section)
        # Check command groups for required args too
        if hasattr(subparser, '_command_details'):
          for cmd_info in subparser._command_details.values():
            if cmd_info.get('type') == 'command' and 'function' in cmd_info:
              # This is a bit tricky - we'd need to check the function signature
              # For now, assume nested commands might have required args
              has_required_args = True

    # Add footnote if there are required arguments
    if has_required_args:
      parts.append("")  # Empty line before footnote
      # Style the entire footnote to match the required argument asterisks
      if hasattr(self, '_theme') and self._theme:
        from .theme import ColorFormatter
        color_formatter = ColorFormatter()
        styled_footnote = color_formatter.apply_style("* - required", self._theme.required_asterisk)
        parts.append(styled_footnote)
      else:
        parts.append("* - required")

    return "\n".join(parts)

  def _format_command_with_args_global(self, name, parser, base_indent, unified_cmd_desc_column, global_option_column):
    """Format a command with unified command description column alignment."""
    lines = []

    # Get required and optional arguments
    required_args, optional_args = self._analyze_arguments(parser)

    # Command line (keep name only, move required args to separate lines)
    command_name = name

    # These are flat commands when using this method
    name_style = 'command_name'
    desc_style = 'command_description'

    # Format description for flat command (with colon and unified column alignment)
    help_text = parser.description or getattr(parser, 'help', '')
    styled_name = self._apply_style(command_name, name_style)

    if help_text:
      # Use unified command description column for consistent alignment
      formatted_lines = self._format_inline_description(
        name=command_name,
        description=help_text,
        name_indent=base_indent,
        description_column=unified_cmd_desc_column,  # Use unified column for consistency
        style_name=name_style,
        style_description=desc_style,
        add_colon=True
      )
      lines.extend(formatted_lines)
    else:
      # Just the command name with styling
      lines.append(f"{' ' * base_indent}{styled_name}")

    # Add required arguments as a list (now on separate lines)
    if required_args:
      for arg_name, arg_help in required_args:
        if arg_help:
          # Required argument with description
          opt_lines = self._format_inline_description(
            name=arg_name,
            description=arg_help,
            name_indent=self._arg_indent + 2,  # Required flat command options +2 spaces (entire line)
            description_column=unified_cmd_desc_column + 4,  # Required flat command option descriptions +4 spaces (2 for line + 2 for desc)
            style_name='option_name',
            style_description='option_description'
          )
          lines.extend(opt_lines)
          # Add asterisk to the last line
          if opt_lines:
            styled_asterisk = self._apply_style(" *", 'required_asterisk')
            lines[-1] += styled_asterisk
        else:
          # Required argument without description - just name and asterisk
          styled_req = self._apply_style(arg_name, 'option_name')
          styled_asterisk = self._apply_style(" *", 'required_asterisk')
          lines.append(f"{' ' * (self._arg_indent + 2)}{styled_req}{styled_asterisk}")  # Flat command options +2 spaces

    # Add optional arguments with unified command description column alignment
    if optional_args:
      for arg_name, arg_help in optional_args:
        styled_opt = self._apply_style(arg_name, 'option_name')
        if arg_help:
          # Use unified command description column for ALL descriptions (commands and options)
          # Option descriptions should be indented 2 more spaces than option names
          opt_lines = self._format_inline_description(
            name=arg_name,
            description=arg_help,
            name_indent=self._arg_indent + 2,  # Flat command options +2 spaces (entire line)
            description_column=unified_cmd_desc_column + 4,  # Flat command option descriptions +4 spaces (2 for line + 2 for desc)
            style_name='option_name',
            style_description='option_description'
          )
          lines.extend(opt_lines)
        else:
          # Just the option name with styling
          lines.append(f"{' ' * (self._arg_indent + 2)}{styled_opt}")  # Flat command options +2 spaces

    return lines

  def _format_group_with_command_groups_global(self, name, parser, base_indent, unified_cmd_desc_column,
                                            global_option_column):
    """Format a command group with unified command description column alignment."""
    lines = []
    indent_str = " " * base_indent

    # Group header with special styling for group commands
    styled_group_name = self._apply_style(name, 'grouped_command_name')

    # Check for CommandGroup description
    group_description = getattr(parser, '_command_group_description', None)
    if group_description:
      # Use unified command description column for consistent formatting
      # Top-level group command descriptions use standard column (no extra indent)
      formatted_lines = self._format_inline_description(
        name=name,
        description=group_description,
        name_indent=base_indent,
        description_column=unified_cmd_desc_column,  # Top-level group commands use standard column
        style_name='grouped_command_name',
        style_description='command_description',  # Reuse command description style
        add_colon=True
      )
      lines.extend(formatted_lines)
    else:
      # Default group display
      lines.append(f"{indent_str}{styled_group_name}")

      # Group description
      help_text = parser.description or getattr(parser, 'help', '')
      if help_text:
        # Top-level group descriptions use standard indent (no extra spaces)
        wrapped_desc = self._wrap_text(help_text, self._desc_indent, self._console_width)
        lines.extend(wrapped_desc)

    # Add sub-global options from the group parser (inner class constructor args)
    # Group command options use same base indentation but descriptions are +2 spaces
    required_args, optional_args = self._analyze_arguments(parser)
    if required_args or optional_args:
      # Add required arguments
      if required_args:
        for arg_name, arg_help in required_args:
          if arg_help:
            # Required argument with description
            opt_lines = self._format_inline_description(
              name=arg_name,
              description=arg_help,
              name_indent=self._arg_indent,  # Required group options at base arg indent
              description_column=unified_cmd_desc_column + 2,  # Required group option descriptions +2 spaces for desc
              style_name='command_group_option_name',
              style_description='command_group_option_description'
            )
            lines.extend(opt_lines)
            # Add asterisk to the last line
            if opt_lines:
              styled_asterisk = self._apply_style(" *", 'required_asterisk')
              lines[-1] += styled_asterisk
          else:
            # Required argument without description - just name and asterisk
            styled_req = self._apply_style(arg_name, 'command_group_option_name')
            styled_asterisk = self._apply_style(" *", 'required_asterisk')
            lines.append(f"{' ' * self._arg_indent}{styled_req}{styled_asterisk}")  # Group options at base indent

      # Add optional arguments
      if optional_args:
        for arg_name, arg_help in optional_args:
          styled_opt = self._apply_style(arg_name, 'command_group_option_name')
          if arg_help:
            # Use unified command description column for sub-global options
            # Group command option descriptions should be indented 2 more spaces
            opt_lines = self._format_inline_description(
              name=arg_name,
              description=arg_help,
              name_indent=self._arg_indent,  # Group options at base arg indent
              description_column=unified_cmd_desc_column + 2,  # Group option descriptions +2 spaces for desc
              style_name='command_group_option_name',
              style_description='command_group_option_description'
            )
            lines.extend(opt_lines)
          else:
            # Just the option name with styling
            lines.append(f"{' ' * self._arg_indent}{styled_opt}")  # Group options at base indent

    # Find and format command groups with unified command description column alignment
    if hasattr(parser, '_commands'):
      command_indent = base_indent + 2

      command_items = sorted(parser._commands.items()) if self._alphabetize else list(parser._commands.items())
      for cmd, cmd_help in command_items:
        # Find the actual subparser
        cmd_parser = self._find_subparser(parser, cmd)
        if cmd_parser:
          # Check if this is a nested group or a final command
          if (hasattr(cmd_parser, '_command_type') and 
              getattr(cmd_parser, '_command_type') == 'group' and
              hasattr(cmd_parser, '_commands') and 
              cmd_parser._commands):
            # This is a nested group - format it as a group recursively
            cmd_section = self._format_group_with_command_groups_global(
              cmd, cmd_parser, command_indent,
              unified_cmd_desc_column, global_option_column
            )
          else:
            # This is a final command - format it as a command
            cmd_section = self._format_command_with_args_global_command(
              cmd, cmd_parser, command_indent,
              unified_cmd_desc_column, global_option_column
            )
          lines.extend(cmd_section)
        else:
          # Fallback for cases where we can't find the parser
          lines.append(f"{' ' * command_indent}{cmd}")
          if cmd_help:
            wrapped_help = self._wrap_text(cmd_help, command_indent + 2, self._console_width)
            lines.extend(wrapped_help)

    return lines

  def _calculate_group_dynamic_columns(self, group_parser, cmd_indent, opt_indent):
    """Calculate dynamic columns for an entire group of command groups."""
    max_cmd_width = 0
    max_opt_width = 0

    # Analyze all command groups in the group
    if hasattr(group_parser, '_commands'):
      for cmd_name in group_parser._commands.keys():
        cmd_parser = self._find_subparser(group_parser, cmd_name)
        if cmd_parser:
          # Check command name width
          cmd_width = len(cmd_name) + cmd_indent
          max_cmd_width = max(max_cmd_width, cmd_width)

          # Check option widths
          _, optional_args = self._analyze_arguments(cmd_parser)
          for arg_name, _ in optional_args:
            opt_width = len(arg_name) + opt_indent
            max_opt_width = max(max_opt_width, opt_width)

    # Calculate description columns with padding
    cmd_desc_column = max_cmd_width + 4  # 4 spaces padding
    opt_desc_column = max_opt_width + 4  # 4 spaces padding

    # Ensure we don't exceed terminal width (leave room for descriptions)
    max_cmd_desc = min(cmd_desc_column, self._console_width // 2)
    max_opt_desc = min(opt_desc_column, self._console_width // 2)

    # Ensure option descriptions are at least 2 spaces more indented than command descriptions
    if max_opt_desc <= max_cmd_desc + 2:
      max_opt_desc = max_cmd_desc + 2

    return max_cmd_desc, max_opt_desc

  def _format_command_with_args_global_command(self, name, parser, base_indent, unified_cmd_desc_column,
                                                  global_option_column):
    """Format a command group with unified command description column alignment."""
    lines = []

    # Get required and optional arguments
    required_args, optional_args = self._analyze_arguments(parser)

    # Command line (keep name only, move required args to separate lines)
    command_name = name

    # These are always command groups when using this method
    name_style = 'command_group_name'
    desc_style = 'grouped_command_description'

    # Format description with unified command description column for consistency
    help_text = parser.description or getattr(parser, 'help', '')
    styled_name = self._apply_style(command_name, name_style)

    if help_text:
      # Use unified command description column for consistent alignment with all commands
      # Command group command descriptions should be indented 2 more spaces
      formatted_lines = self._format_inline_description(
        name=command_name,
        description=help_text,
        name_indent=base_indent,
        description_column=unified_cmd_desc_column + 2,  # Command group command descriptions +2 more spaces
        style_name=name_style,
        style_description=desc_style,
        add_colon=True  # Add colon for command groups
      )
      lines.extend(formatted_lines)
    else:
      # Just the command name with styling
      lines.append(f"{' ' * base_indent}{styled_name}")

    # Add required arguments as a list (now on separate lines)
    if required_args:
      for arg_name, arg_help in required_args:
        if arg_help:
          # Required argument with description
          opt_lines = self._format_inline_description(
            name=arg_name,
            description=arg_help,
            name_indent=self._arg_indent + 2,  # Required command group options +2 spaces (entire line)
            description_column=unified_cmd_desc_column + 4,  # Required command group option descriptions +4 spaces (2 for line + 2 for desc)
            style_name='option_name',
            style_description='option_description'
          )
          lines.extend(opt_lines)
          # Add asterisk to the last line
          if opt_lines:
            styled_asterisk = self._apply_style(" *", 'required_asterisk')
            lines[-1] += styled_asterisk
        else:
          # Required argument without description - just name and asterisk
          styled_req = self._apply_style(arg_name, 'option_name')
          styled_asterisk = self._apply_style(" *", 'required_asterisk')
          lines.append(f"{' ' * (self._arg_indent + 2)}{styled_req}{styled_asterisk}")  # Command group options +2 spaces

    # Add optional arguments with unified command description column alignment
    if optional_args:
      for arg_name, arg_help in optional_args:
        styled_opt = self._apply_style(arg_name, 'option_name')
        if arg_help:
          # Use unified command description column for ALL descriptions (commands and options)
          # Command group command option descriptions should be indented 2 more spaces
          opt_lines = self._format_inline_description(
            name=arg_name,
            description=arg_help,
            name_indent=self._arg_indent + 2,  # Command group options +2 spaces (entire line)
            description_column=unified_cmd_desc_column + 4,  # Command group option descriptions +4 spaces (2 for line + 2 for desc)
            style_name='option_name',
            style_description='option_description'
          )
          lines.extend(opt_lines)
        else:
          # Just the option name with styling
          lines.append(f"{' ' * (self._arg_indent + 2)}{styled_opt}")  # Command group options +2 spaces

    return lines

  def _analyze_arguments(self, parser):
    """Analyze parser arguments and return required and optional separately."""
    if not parser:
      return [], []

    required_args = []
    optional_args = []

    for action in parser._actions:
      if action.dest == 'help':
        continue

      # Handle sub-global arguments specially (they have _subglobal_ prefix)
      clean_param_name = None
      if action.dest.startswith('_subglobal_'):
        # Extract the clean parameter name from _subglobal_command-name_param_name
        # Example: _subglobal_file-operations_work_dir -> work_dir -> work-dir
        parts = action.dest.split('_', 3)  # Split into ['', 'subglobal', 'command-name', 'param_name']
        if len(parts) >= 4:
          clean_param_name = parts[3]  # Get the actual parameter name
          arg_name = f"--{clean_param_name.replace('_', '-')}"
        else:
          # Fallback for unexpected format
          arg_name = f"--{action.dest.replace('_', '-')}"
      else:
        arg_name = f"--{action.dest.replace('_', '-')}"

      arg_help = getattr(action, 'help', '')

      if hasattr(action, 'required') and action.required:
        # Required argument - we'll add styled asterisk later in formatting
        if hasattr(action, 'metavar') and action.metavar:
          required_args.append((f"{arg_name} {action.metavar}", arg_help))
        else:
          # Use clean parameter name for metavar if available, otherwise use dest
          metavar_base = clean_param_name if clean_param_name else action.dest
          required_args.append((f"{arg_name} {metavar_base.upper()}", arg_help))
      elif action.option_strings:
        # Optional argument - add to list display
        if action.nargs == 0 or getattr(action, 'action', None) == 'store_true':
          # Boolean flag
          optional_args.append((arg_name, arg_help))
        else:
          # Value argument
          if hasattr(action, 'metavar') and action.metavar:
            arg_display = f"{arg_name} {action.metavar}"
          else:
            # Use clean parameter name for metavar if available, otherwise use dest
            metavar_base = clean_param_name if clean_param_name else action.dest
            arg_display = f"{arg_name} {metavar_base.upper()}"
          optional_args.append((arg_display, arg_help))

    # Sort arguments alphabetically if alphabetize is enabled
    if self._alphabetize:
      required_args.sort(key=lambda x: x[0])  # Sort by argument name (first element of tuple)
      optional_args.sort(key=lambda x: x[0])  # Sort by argument name (first element of tuple)

    return required_args, optional_args

  def _wrap_text(self, text, indent, width):
    """Wrap text with proper indentation using textwrap."""
    if not text:
      return []

    # Calculate available width for text
    available_width = max(width - indent, 20)  # Minimum 20 chars

    # Use textwrap to handle the wrapping
    wrapper = textwrap.TextWrapper(
      width=available_width,
      initial_indent=" " * indent,
      subsequent_indent=" " * indent,
      break_long_words=False,
      break_on_hyphens=False
    )

    return wrapper.wrap(text)

  def _apply_style(self, text: str, style_name: str) -> str:
    """Apply theme style to text if theme is available."""
    if not self._theme or not self._color_formatter:
      return text

    # Map style names to theme attributes
    style_map = {
      'title': self._theme.title,
      'subtitle': self._theme.subtitle,
      'command_name': self._theme.command_name,
      'command_description': self._theme.command_description,
      # Command Group Level (inner class level)
      'command_group_name': self._theme.command_group_name,
      'command_group_description': self._theme.command_group_description,
      'command_group_option_name': self._theme.command_group_option_name,
      'command_group_option_description': self._theme.command_group_option_description,
      # Grouped Command Level (commands within the group)
      'grouped_command_name': self._theme.grouped_command_name,
      'grouped_command_description': self._theme.grouped_command_description,
      'grouped_command_option_name': self._theme.grouped_command_option_name,
      'grouped_command_option_description': self._theme.grouped_command_option_description,
      'option_name': self._theme.option_name,
      'option_description': self._theme.option_description,
      'required_asterisk': self._theme.required_asterisk
    }

    style = style_map.get(style_name)
    if style:
      return self._color_formatter.apply_style(text, style)
    return text

  def _get_display_width(self, text: str) -> int:
    """Get display width of text, handling ANSI color codes."""
    if not text:
      return 0

    # Strip ANSI escape sequences for width calculation
    import re
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    clean_text = ansi_escape.sub('', text)
    return len(clean_text)

  def _format_inline_description(
      self,
      name: str,
      description: str,
      name_indent: int,
      description_column: int,
      style_name: str,
      style_description: str,
      add_colon: bool = False
  ) -> list[str]:
    """Format name and description inline with consistent wrapping.

    :param name: The command/option name to display
    :param description: The description text
    :param name_indent: Indentation for the name
    :param description_column: Column where description should start
    :param style_name: Theme style for the name
    :param style_description: Theme style for the description
    :return: List of formatted lines
    """
    lines = []
    
    if not description:
      # No description, just return the styled name (with colon if requested)
      styled_name = self._apply_style(name, style_name)
      display_name = f"{styled_name}:" if add_colon else styled_name
      lines = [f"{' ' * name_indent}{display_name}"]
    else:
      styled_name = self._apply_style(name, style_name)
      styled_description = self._apply_style(description, style_description)

      # Create the full line with proper spacing (add colon if requested)
      display_name = f"{styled_name}:" if add_colon else styled_name
      name_part = f"{' ' * name_indent}{display_name}"
      name_display_width = name_indent + self._get_display_width(name) + (1 if add_colon else 0)

      # Calculate spacing needed to reach description column
      # All descriptions (commands, command groups, and options) use the same column alignment
      spacing_needed = description_column - name_display_width
      spacing = description_column

      if name_display_width >= description_column:
        # Name is too long, use minimum spacing (4 spaces)
        spacing_needed = 4
        spacing = name_display_width + spacing_needed

      # Try to fit everything on first line
      first_line = f"{name_part}{' ' * spacing_needed}{styled_description}"

      # Check if first line fits within console width
      if self._get_display_width(first_line) <= self._console_width:
        # Everything fits on one line
        lines = [first_line]
      else:
        # Need to wrap - start with name and first part of description on same line
        available_width_first_line = self._console_width - name_display_width - spacing_needed

        if available_width_first_line >= 20:  # Minimum readable width for first line
          # For wrapping, we need to work with the unstyled description text to get proper line breaks
          # then apply styling to each wrapped line
          wrapper = textwrap.TextWrapper(
            width=available_width_first_line,
            break_long_words=False,
            break_on_hyphens=False
          )
          desc_lines = wrapper.wrap(description)  # Use unstyled description for accurate wrapping

          if desc_lines:
            # First line with name and first part of description (apply styling to first line)
            styled_first_desc = self._apply_style(desc_lines[0], style_description)
            lines = [f"{name_part}{' ' * spacing_needed}{styled_first_desc}"]

            # Continuation lines with remaining description
            if len(desc_lines) > 1:
              # Calculate where the description text actually starts on the first line
              desc_start_position = name_display_width + spacing_needed
              continuation_indent = " " * desc_start_position
              for desc_line in desc_lines[1:]:
                styled_desc_line = self._apply_style(desc_line, style_description)
                lines.append(f"{continuation_indent}{styled_desc_line}")
        
        if not lines:  # Fallback if wrapping didn't work
          # Fallback: put description on separate lines (name too long or not enough space)
          lines = [name_part]

          # All descriptions (commands, command groups, and options) use the same alignment
          desc_indent = spacing

          available_width = self._console_width - desc_indent
          if available_width < 20:  # Minimum readable width
            available_width = 20
            desc_indent = self._console_width - available_width

          # Wrap the description text (use unstyled text for accurate wrapping)
          wrapper = textwrap.TextWrapper(
            width=available_width,
            break_long_words=False,
            break_on_hyphens=False
          )

          desc_lines = wrapper.wrap(description)  # Use unstyled description for accurate wrapping
          indent_str = " " * desc_indent

          for desc_line in desc_lines:
            styled_desc_line = self._apply_style(desc_line, style_description)
            lines.append(f"{indent_str}{styled_desc_line}")

    return lines

  def _format_usage(self, usage, actions, groups, prefix):
    """Override to add color to usage line and potentially title."""
    usage_text = super()._format_usage(usage, actions, groups, prefix)

    # If this is the main parser (not a subparser), prepend styled title
    if prefix == 'usage: ' and hasattr(self, '_root_section'):
      # Try to get the parser description (title)
      parser = getattr(self._root_section, 'formatter', None)
      if parser:
        parser_obj = getattr(parser, '_parser', None)
        if parser_obj and hasattr(parser_obj, 'description') and parser_obj.description:
          styled_title = self._apply_style(parser_obj.description, 'title')
          return f"{styled_title}\n\n{usage_text}"

    return usage_text

  def start_section(self, heading):
    """Override to customize section headers with theming and capitalization."""
    if heading and heading.lower() == 'options':
      # Capitalize options to OPTIONS and apply subtitle theme
      styled_heading = self._apply_style('OPTIONS', 'subtitle')
      super().start_section(styled_heading)
    elif heading and heading == 'COMMANDS':
      # Apply subtitle theme to COMMANDS
      styled_heading = self._apply_style('COMMANDS', 'subtitle')
      super().start_section(styled_heading)
    else:
      # For other sections, apply subtitle theme if available
      if heading and self._theme:
        styled_heading = self._apply_style(heading, 'subtitle')
        super().start_section(styled_heading)
      else:
        super().start_section(heading)

  def _find_subparser(self, parent_parser, subcmd_name):
    """Find a subparser by name in the parent parser."""
    result = None
    for action in parent_parser._actions:
      if isinstance(action, argparse._SubParsersAction):
        if subcmd_name in action.choices:
          result = action.choices[subcmd_name]
          break
    return result

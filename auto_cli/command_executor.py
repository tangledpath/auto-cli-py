"""Command execution service for CLI applications.

Handles the execution of different command types (direct methods, inner class methods, module functions)
by creating appropriate instances and invoking methods with parsed arguments.
"""

import inspect
from typing import Any, Dict, Type, Optional


class CommandExecutor:
    """Centralized service for executing CLI commands with different patterns."""

    def __init__(self, target_class: Optional[Type] = None, target_module: Optional[Any] = None, 
                 inner_class_metadata: Optional[Dict[str, Dict[str, Any]]] = None):
        """Initialize command executor with target information.
        
        :param target_class: Class containing methods to execute (for class-based CLI)
        :param target_module: Module containing functions to execute (for module-based CLI)
        :param inner_class_metadata: Metadata for inner class commands
        """
        self.target_class = target_class
        self.target_module = target_module
        self.inner_class_metadata = inner_class_metadata or {}

    def execute_inner_class_command(self, parsed) -> Any:
        """Execute command using inner class pattern.
        
        Creates main class instance, inner class instance, then invokes method.
        """
        method = parsed._cli_function
        original_name = parsed._function_name

        # Get metadata for this command
        if original_name not in self.inner_class_metadata:
            raise RuntimeError(f"No metadata found for command: {original_name}")

        metadata = self.inner_class_metadata[original_name]
        inner_class = metadata['inner_class']
        command_name = metadata['command_name']

        # 1. Create main class instance with global arguments
        main_instance = self._create_main_instance(parsed)

        # 2. Create inner class instance with sub-global arguments
        inner_instance = self._create_inner_instance(inner_class, command_name, parsed, main_instance)

        # 3. Execute method with command arguments
        return self._execute_method(inner_instance, metadata['method_name'], parsed)

    def execute_direct_method_command(self, parsed) -> Any:
        """Execute command using direct method from class.
        
        Creates class instance with parameterless constructor, then invokes method.
        """
        method = parsed._cli_function

        # Create class instance (requires parameterless constructor or all defaults)
        try:
            class_instance = self.target_class()
        except TypeError as e:
            raise RuntimeError(
                f"Cannot instantiate {self.target_class.__name__}: constructor parameters must have default values") from e

        # Execute method with arguments
        return self._execute_method(class_instance, method.__name__, parsed)

    def execute_module_function(self, parsed) -> Any:
        """Execute module function directly.
        
        Invokes function from module with parsed arguments.
        """
        function = parsed._cli_function
        return self._execute_function(function, parsed)

    def _create_main_instance(self, parsed) -> Any:
        """Create main class instance with global arguments."""
        main_kwargs = {}
        main_sig = inspect.signature(self.target_class.__init__)

        for param_name, param in main_sig.parameters.items():
            if param_name == 'self':
                continue
            if param.kind in (param.VAR_POSITIONAL, param.VAR_KEYWORD):
                continue

            # Look for global argument
            global_attr = f'_global_{param_name}'
            if hasattr(parsed, global_attr):
                value = getattr(parsed, global_attr)
                main_kwargs[param_name] = value

        try:
            return self.target_class(**main_kwargs)
        except TypeError as e:
            raise RuntimeError(f"Cannot instantiate {self.target_class.__name__} with global args: {e}") from e

    def _create_inner_instance(self, inner_class: Type, command_name: str, parsed, main_instance: Any) -> Any:
        """Create inner class instance with sub-global arguments."""
        inner_kwargs = {}
        inner_sig = inspect.signature(inner_class.__init__)

        for param_name, param in inner_sig.parameters.items():
            if param_name == 'self':
                continue
            if param.kind in (param.VAR_POSITIONAL, param.VAR_KEYWORD):
                continue

            # Look for sub-global argument
            subglobal_attr = f'_subglobal_{command_name}_{param_name}'
            if hasattr(parsed, subglobal_attr):
                value = getattr(parsed, subglobal_attr)
                inner_kwargs[param_name] = value

        try:
            return inner_class(main_instance, **inner_kwargs)
        except TypeError as e:
            raise RuntimeError(f"Cannot instantiate {inner_class.__name__} with sub-global args: {e}") from e

    def _execute_method(self, instance: Any, method_name: str, parsed) -> Any:
        """Execute method on instance with parsed arguments."""
        bound_method = getattr(instance, method_name)
        method_kwargs = self._extract_method_arguments(bound_method, parsed)
        return bound_method(**method_kwargs)

    def _execute_function(self, function: Any, parsed) -> Any:
        """Execute function directly with parsed arguments."""
        function_kwargs = self._extract_method_arguments(function, parsed)
        return function(**function_kwargs)

    def _extract_method_arguments(self, method_or_function: Any, parsed) -> Dict[str, Any]:
        """Extract method/function arguments from parsed CLI arguments."""
        sig = inspect.signature(method_or_function)
        kwargs = {}

        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            if param.kind in (param.VAR_POSITIONAL, param.VAR_KEYWORD):
                continue

            # Look for method argument (no prefix, just the parameter name)
            attr_name = param_name.replace('-', '_')
            if hasattr(parsed, attr_name):
                value = getattr(parsed, attr_name)
                kwargs[param_name] = value

        return kwargs

    def execute_command(self, parsed, target_mode, use_inner_class_pattern: bool = False, 
                       inner_class_metadata: Optional[Dict[str, Dict[str, Any]]] = None) -> Any:
        """Main command execution dispatcher - determines execution strategy based on target mode."""
        if target_mode.value == 'module':
            return self.execute_module_function(parsed)
        elif target_mode.value == 'class':
            # Determine if this is an inner class method or direct method
            original_name = getattr(parsed, '_function_name', '')
            
            if (use_inner_class_pattern and
                inner_class_metadata and
                original_name in inner_class_metadata):
                # Execute inner class method
                return self.execute_inner_class_command(parsed)
            else:
                # Execute direct method from class
                return self.execute_direct_method_command(parsed)
        else:
            raise RuntimeError(f"Unknown target mode: {target_mode}")

    def handle_execution_error(self, parsed, error: Exception) -> int:
        """Handle execution errors with appropriate logging and return codes."""
        import sys
        import traceback
        
        function_name = getattr(parsed, '_function_name', 'unknown')
        print(f"Error executing {function_name}: {error}", file=sys.stderr)

        if getattr(parsed, 'verbose', False):
            traceback.print_exc()

        return 1
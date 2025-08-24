"""Argument parsing utilities for CLI generation."""

import argparse
import enum
import inspect
from pathlib import Path
from typing import Any, Dict, Union, get_args, get_origin

from .docstring_parser import extract_function_help


class ArgumentParserService:
    """Centralized service for handling argument parser configuration and setup."""

    @staticmethod
    def get_arg_type_config(annotation: type) -> Dict[str, Any]:
        """Configure argparse arguments based on Python type annotations.
        
        Enables CLI generation from function signatures by mapping Python types to argparse behavior.
        """
        # Handle Optional[Type] -> get the actual type
        # Handle both typing.Union and types.UnionType (Python 3.10+)
        origin = get_origin(annotation)
        if origin is Union or str(origin) == "<class 'types.UnionType'>":
            args = get_args(annotation)
            # Optional[T] is Union[T, NoneType]
            if len(args) == 2 and type(None) in args:
                annotation = next(arg for arg in args if arg is not type(None))

        if annotation in (str, int, float):
            return {'type': annotation}
        elif annotation == bool:
            return {'action': 'store_true'}
        elif annotation == Path:
            return {'type': Path}
        elif inspect.isclass(annotation) and issubclass(annotation, enum.Enum):
            return {
                'type': lambda x: annotation[x.split('.')[-1]],
                'choices': list(annotation),
                'metavar': f"{{{','.join(e.name for e in annotation)}}}"
            }
        return {}

    @staticmethod
    def add_global_class_args(parser: argparse.ArgumentParser, target_class: type) -> None:
        """Enable class-based CLI with global configuration options.
        
        Class constructors define application-wide settings that apply to all commands.
        """
        init_method = target_class.__init__
        sig = inspect.signature(init_method)
        _, param_help = extract_function_help(init_method)

        for param_name, param in sig.parameters.items():
            # Skip self parameter and varargs
            if param_name == 'self' or param.kind in (param.VAR_POSITIONAL, param.VAR_KEYWORD):
                continue

            arg_config = {
                'dest': f'_global_{param_name}',  # Prefix to avoid conflicts
                'help': param_help.get(param_name, f"Global {param_name} parameter")
            }

            # Handle type annotations
            if param.annotation != param.empty:
                type_config = ArgumentParserService.get_arg_type_config(param.annotation)
                arg_config.update(type_config)

            # Handle defaults
            if param.default != param.empty:
                arg_config['default'] = param.default
            else:
                arg_config['required'] = True

            # Add argument without prefix (user requested no global- prefix)
            from .string_utils import StringUtils
            flag_name = StringUtils.clean_parameter_name(param_name)
            flag = f"--{flag_name}"

            # Check for conflicts with built-in CLI options
            built_in_options = {'no-color', 'help'}
            if flag_name not in built_in_options:
                parser.add_argument(flag, **arg_config)

    @staticmethod
    def add_subglobal_class_args(parser: argparse.ArgumentParser, inner_class: type, command_name: str) -> None:
        """Enable command group configuration for hierarchical CLI organization.
        
        Inner class constructors provide group-specific settings shared across related commands.
        """
        init_method = inner_class.__init__
        sig = inspect.signature(init_method)
        _, param_help = extract_function_help(init_method)

        # Get parameters as a list to skip main_instance parameter
        params = list(sig.parameters.items())
        
        # Skip self (index 0) and main_instance (index 1), start from index 2
        for param_name, param in params[2:]:
            # Skip varargs
            if param.kind in (param.VAR_POSITIONAL, param.VAR_KEYWORD):
                continue

            arg_config = {
                'dest': f'_subglobal_{command_name}_{param_name}',  # Prefix to avoid conflicts
                'help': param_help.get(param_name, f"{command_name} {param_name} parameter")
            }

            # Handle type annotations
            if param.annotation != param.empty:
                type_config = ArgumentParserService.get_arg_type_config(param.annotation)
                arg_config.update(type_config)
            
            # Set clean metavar if not already set by type config
            if 'metavar' not in arg_config and 'action' not in arg_config:
                arg_config['metavar'] = param_name.upper()

            # Handle defaults
            if param.default != param.empty:
                arg_config['default'] = param.default
            else:
                arg_config['required'] = True

            # Add argument with command-specific prefix
            from .string_utils import StringUtils
            flag = f"--{StringUtils.clean_parameter_name(param_name)}"
            parser.add_argument(flag, **arg_config)

    @staticmethod
    def add_function_args(parser: argparse.ArgumentParser, fn: Any) -> None:
        """Generate CLI arguments directly from function signatures.
        
        Eliminates manual argument configuration by leveraging Python type hints and docstrings.
        """
        sig = inspect.signature(fn)
        _, param_help = extract_function_help(fn)

        for name, param in sig.parameters.items():
            # Skip self parameter and varargs
            if name == 'self' or param.kind in (param.VAR_POSITIONAL, param.VAR_KEYWORD):
                continue

            arg_config: Dict[str, Any] = {
                'dest': name,
                'help': param_help.get(name, f"{name} parameter")
            }

            # Handle type annotations
            if param.annotation != param.empty:
                type_config = ArgumentParserService.get_arg_type_config(param.annotation)
                arg_config.update(type_config)

            # Handle defaults - determine if argument is required
            if param.default != param.empty:
                arg_config['default'] = param.default
                # Don't set required for optional args
            else:
                arg_config['required'] = True

            # Add argument with kebab-case flag name
            from .string_utils import StringUtils
            flag = f"--{StringUtils.clean_parameter_name(name)}"
            parser.add_argument(flag, **arg_config)
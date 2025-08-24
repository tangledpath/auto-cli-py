"""Validation utilities for CLI generation and parameter checking."""

import inspect
from typing import Any, List, Type


class ValidationService:
    """Centralized validation service for CLI parameter and constructor validation."""

    @staticmethod
    def validate_constructor_parameters(cls: Type, context: str, allow_parameterless_only: bool = False) -> None:
        """Validate constructor compatibility for CLI argument generation.

        CLI must instantiate classes during command execution - constructor parameters become CLI arguments.
        
        :param cls: The class to validate
        :param context: Context string for error messages (e.g., "main class", "inner class 'UserOps'")
        :param allow_parameterless_only: If True, allows only parameterless constructors (for direct method pattern)
        :raises ValueError: If constructor has parameters without defaults
        """
        try:
            init_method = cls.__init__
            sig = inspect.signature(init_method)
            params_without_defaults = []

            for param_name, param in sig.parameters.items():
                # Skip self parameter and varargs
                if param_name == 'self' or param.kind in (param.VAR_POSITIONAL, param.VAR_KEYWORD):
                    continue

                # Check if parameter has no default value
                if param.default == param.empty:
                    params_without_defaults.append(param_name)

            if params_without_defaults:
                param_list = ', '.join(params_without_defaults)
                class_name = cls.__name__
                
                if allow_parameterless_only:
                    error_msg = (f"Constructor for {context} '{class_name}' has parameters without default values: {param_list}. "
                               "For classes using direct methods, the constructor must be parameterless or all parameters must have default values.")
                else:
                    error_msg = (f"Constructor for {context} '{class_name}' has parameters without default values: {param_list}. "
                               "All constructor parameters must have default values to be used as CLI arguments.")
                raise ValueError(error_msg)

        except Exception as e:
            # Re-raise ValueError as-is, others as ValueError with context
            error_to_raise = e if isinstance(e, ValueError) else ValueError(f"Error validating constructor for {context} '{cls.__name__}': {e}")
            if not isinstance(e, ValueError):
                error_to_raise.__cause__ = e
            raise error_to_raise

    @staticmethod
    def validate_inner_class_constructor_parameters(cls: Type, context: str) -> None:
        """Inner classes need main instance injection while supporting optional sub-global arguments."""
        try:
            init_method = cls.__init__
            sig = inspect.signature(init_method)
            params = list(sig.parameters.items())
            params_without_defaults = []
            
            # First parameter should be 'self'
            if not params or params[0][0] != 'self':
                raise ValueError(f"Constructor for {context} '{cls.__name__}' is malformed (missing self parameter)")
            
            # Determine if this follows the new main_instance pattern or old pattern
            if len(params) >= 2:
                # Check if second parameter is likely main_instance (no type annotation for main_instance is expected)
                second_param_name, second_param = params[1]
                
                # If second parameter has no default and no annotation, assume it's main_instance
                if (second_param.default == second_param.empty and 
                    second_param.annotation == second_param.empty):
                    # New pattern: main_instance parameter - check remaining params for defaults
                    for param_name, param in params[2:]:  # Skip 'self' and main_instance
                        if param.kind in (param.VAR_POSITIONAL, param.VAR_KEYWORD):
                            continue
                        if param.default == param.empty:
                            params_without_defaults.append(param_name)
                else:
                    # Old pattern or malformed: all params after self need defaults
                    for param_name, param in params[1:]:  # Skip only 'self'
                        if param.kind in (param.VAR_POSITIONAL, param.VAR_KEYWORD):
                            continue
                        if param.default == param.empty:
                            params_without_defaults.append(param_name)
            else:
                # Only self parameter - this is valid (no sub-global args)
                pass
            
            if params_without_defaults:
                param_list = ', '.join(params_without_defaults)
                class_name = cls.__name__
                error_msg = (f"Constructor for {context} '{class_name}' has parameters without default values: {param_list}. "
                           f"All constructor parameters must have default values to be used as CLI arguments.")
                raise ValueError(error_msg)
                
        except Exception as e:
            # Re-raise ValueError as-is, others as ValueError with context
            error_to_raise = e if isinstance(e, ValueError) else ValueError(f"Error validating inner class constructor for {context} '{cls.__name__}': {e}")
            if not isinstance(e, ValueError):
                error_to_raise.__cause__ = e
            raise error_to_raise

    @staticmethod
    def validate_function_signature(func: Any) -> bool:
        """Type annotations enable automatic CLI argument type mapping without manual configuration."""
        try:
            sig = inspect.signature(func)
            
            # Check each parameter has compatible type annotation
            for param_name, param in sig.parameters.items():
                # Skip self parameter and varargs
                if param_name == 'self' or param.kind in (param.VAR_POSITIONAL, param.VAR_KEYWORD):
                    continue
                
                # Function must have type annotations for CLI generation
                if param.annotation == param.empty:
                    return False
                    
            return True
            
        except (ValueError, TypeError):
            return False

    @staticmethod
    def get_validation_errors(cls: Type, functions: dict[str, Any]) -> List[str]:
        """Early validation prevents runtime failures during CLI generation and command execution."""
        errors = []
        
        # Validate class constructor if provided
        if cls:
            try:
                ValidationService.validate_constructor_parameters(cls, "main class")
            except ValueError as e:
                errors.append(str(e))
        
        # Validate each function
        for func_name, func in functions.items():
            if not ValidationService.validate_function_signature(func):
                errors.append(f"Function '{func_name}' has invalid signature for CLI generation")
        
        return errors
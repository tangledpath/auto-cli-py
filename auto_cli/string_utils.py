"""Centralized string utilities for CLI generation with caching."""

from functools import lru_cache
from typing import Dict


class StringUtils:
    """Centralized string conversion utilities with performance optimizations."""
    
    # Cache for converted strings to avoid repeated operations
    _conversion_cache: Dict[str, str] = {}
    
    @staticmethod
    @lru_cache(maxsize=256)
    def snake_to_kebab(text: str) -> str:
        """Convert Python naming to CLI-friendly format.
        
        CLI conventions favor kebab-case for better readability and consistency across shells.
        """
        return text.replace('_', '-')
    
    @staticmethod
    @lru_cache(maxsize=256) 
    def kebab_to_snake(text: str) -> str:
        """Map CLI argument names back to Python function parameters.
        
        Enables seamless integration between CLI parsing and function invocation.
        """
        return text.replace('-', '_')
    
    @staticmethod
    @lru_cache(maxsize=256)
    def clean_parameter_name(param_name: str) -> str:
        """Normalize parameter names for consistent CLI interface.
        
        Ensures uniform argument naming regardless of Python coding style variations.
        """
        return param_name.replace('_', '-').lower()
    
    @staticmethod
    def clear_cache() -> None:
        """Reset string conversion cache for testing isolation.
        
        Prevents test interdependencies by ensuring clean state between test runs.
        """
        StringUtils.snake_to_kebab.cache_clear()
        StringUtils.kebab_to_snake.cache_clear() 
        StringUtils.clean_parameter_name.cache_clear()
        StringUtils._conversion_cache.clear()
    
    @staticmethod
    def get_cache_info() -> dict:
        """Get cache statistics for performance monitoring."""
        return {
            'snake_to_kebab': StringUtils.snake_to_kebab.cache_info()._asdict(),
            'kebab_to_snake': StringUtils.kebab_to_snake.cache_info()._asdict(),
            'clean_parameter_name': StringUtils.clean_parameter_name.cache_info()._asdict(),
            'conversion_cache_size': len(StringUtils._conversion_cache)
        }
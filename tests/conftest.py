"""Test configuration and fixtures for auto-cli-py tests."""
import enum
import sys
from pathlib import Path

import pytest


class TestEnum(enum.Enum):
  """Test enumeration for CLI testing."""
  OPTION_A = 1
  OPTION_B = 2
  OPTION_C = 3


def sample_function(name: str = "world", count: int = 1):
  """Sample function with docstring parameters.

  :param name: The name to greet in the message
  :param count: Number of times to repeat the greeting
  """
  return f"Hello {name}! " * count


def function_with_types(
    text: str,
    number: int = 42,
    ratio: float = 3.14,
    active: bool = False,
    choice: TestEnum = TestEnum.OPTION_A,
    file_path: Path | None = None
):
  """Function with various type annotations.

  :param text: Required text input parameter
  :param number: Optional integer with default value
  :param ratio: Optional float with default value
  :param active: Boolean flag parameter
  :param choice: Enumeration choice parameter
  :param file_path: Optional file path parameter
  """
  return {
    'text': text,
    'number': number,
    'ratio': ratio,
    'active': active,
    'choice': choice,
    'file_path': file_path
  }


def function_without_docstring():
  """Function without parameter docstrings."""
  return "No docstring parameters"


def function_with_args_kwargs(required: str, *args, **kwargs):
  """Function with *args and **kwargs.

  :param required: Required parameter
  """
  return f"Required: {required}, args: {args}, kwargs: {kwargs}"


@pytest.fixture
def sample_module():
  """Provide a sample module for testing."""
  return sys.modules[__name__]


@pytest.fixture
def sample_function_opts():
  """Provide sample function options for backward compatibility tests."""
  return {
    'sample_function': {'description': 'Sample function for testing'},
    'function_with_types': {'description': 'Function with various types'}
  }

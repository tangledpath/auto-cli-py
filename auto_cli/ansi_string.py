"""ANSI-aware string wrapper for proper alignment in format strings.

This module provides the AnsiString class which enables proper text alignment
in f-strings and format() calls when working with ANSI escape codes for terminal colors.
"""

import re
from typing import Union

# Regex pattern to match ANSI escape sequences
ANSI_ESCAPE_PATTERN = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')


def strip_ansi_codes(text: str) -> str:
  """Remove ANSI escape sequences from text to get visible character count.

  :param text: Text that may contain ANSI escape codes
  :return: Text with ANSI codes removed
  """
  return ANSI_ESCAPE_PATTERN.sub('', text) if text else ''


class AnsiString:
  """String wrapper that implements proper alignment with ANSI escape codes.

  This class wraps a string containing ANSI escape codes and provides
  a __format__ method that correctly handles alignment by considering
  only the visible characters when calculating padding.

  Example:
      >>> colored_text = '\\033[31mRed Text\\033[0m'  # Red colored text
      >>> f"{AnsiString(colored_text):>10}"  # Right-align in 10 characters
      '   \\033[31mRed Text\\033[0m'  # Only 'Red Text' counted for alignment
  """

  def __init__(self, text: str):
    """Initialize with text that may contain ANSI escape codes.

    :param text: The string to wrap (may contain ANSI codes)
    """
    self.text = text if text is not None else ''
    self._visible_text = strip_ansi_codes(self.text)

  def __str__(self) -> str:
    """Return the original text with ANSI codes intact."""
    return self.text

  def __repr__(self) -> str:
    """Return debug representation."""
    return f"AnsiString({self.text!r})"

  def __len__(self) -> int:
    """Return the visible character count (excluding ANSI codes)."""
    return len(self._visible_text)

  def __format__(self, format_spec: str) -> str:
    """Format the string with proper ANSI-aware alignment.

    This method implements Python's format protocol to handle alignment
    correctly when the string contains ANSI escape codes.

    :param format_spec: Format specification (e.g., '<10', '>20', '^15')
    :return: Formatted string with proper alignment
    """
    if not format_spec:
      return self.text

    # Parse the format specification
    # Format: [fill][align][width]
    fill_char = ' '
    align = '<'  # Default alignment
    width = 0

    # Extract components from format_spec
    spec = format_spec.strip()

    if not spec:
      return self.text

    # Check for fill character and alignment
    if len(spec) >= 2 and spec[1] in '<>=^':
      fill_char = spec[0]
      align = spec[1]
      width_str = spec[2:]
    elif len(spec) >= 1 and spec[0] in '<>=^':
      align = spec[0]
      width_str = spec[1:]
    else:
      # No alignment specified, assume width only
      width_str = spec

    # Parse width
    try:
      width = int(width_str) if width_str else 0
    except ValueError:
      # Invalid format spec, return original text
      return self.text

    # Calculate visible length and required padding
    visible_length = len(self._visible_text)

    if width <= visible_length:
      # No padding needed
      return self.text

    padding_needed = width - visible_length

    # Apply alignment
    if align == '<':  # Left align
      return self.text + (fill_char * padding_needed)
    elif align == '>':  # Right align
      return (fill_char * padding_needed) + self.text
    elif align == '^':  # Center align
      left_padding = padding_needed // 2
      right_padding = padding_needed - left_padding
      return (fill_char * left_padding) + self.text + (fill_char * right_padding)
    elif align == '=':  # Sign-aware padding (treat like right align for text)
      return (fill_char * padding_needed) + self.text
    else:
      # Unknown alignment, return original
      return self.text

  def __eq__(self, other) -> bool:
    """Check equality based on the original text."""
    if isinstance(other, AnsiString):
      return self.text == other.text
    elif isinstance(other, str):
      return self.text == other
    return False

  def __hash__(self) -> int:
    """Make AnsiString hashable based on original text."""
    return hash(self.text)

  @property
  def visible_text(self) -> str:
    """Get the text with ANSI codes stripped (visible characters only)."""
    return self._visible_text

  @property
  def visible_length(self) -> int:
    """Get the visible character count (excluding ANSI codes)."""
    return len(self._visible_text)

  def startswith(self, prefix: Union[str, 'AnsiString']) -> bool:
    """Check if visible text starts with prefix."""
    prefix_str = prefix.visible_text if isinstance(prefix, AnsiString) else str(prefix)
    return self._visible_text.startswith(prefix_str)

  def endswith(self, suffix: Union[str, 'AnsiString']) -> bool:
    """Check if visible text ends with suffix."""
    suffix_str = suffix.visible_text if isinstance(suffix, AnsiString) else str(suffix)
    return self._visible_text.endswith(suffix_str)

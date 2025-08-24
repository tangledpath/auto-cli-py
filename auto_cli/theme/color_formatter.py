"""Handles color application and terminal compatibility."""
from __future__ import annotations

import sys
from typing import Union

from auto_cli.theme.enums import Style
from auto_cli.theme.rgb import RGB
from auto_cli.theme.theme_style import ThemeStyle


class ColorFormatter:
  """Handles color application and terminal compatibility."""

  def __init__(self, enable_colors: Union[bool, None] = None):
    """Initialize color formatter with automatic color detection.

    :param enable_colors: Force enable/disable colors, or None for auto-detection
    """
    self.colors_enabled = self._is_color_terminal() if enable_colors is None else enable_colors

    if self.colors_enabled:
      self.enable_windows_ansi_support()

  @staticmethod
  def enable_windows_ansi_support():
    """Enable ANSI escape sequences on Windows terminals."""
    if sys.platform != 'win32':
      return

    try:
      import ctypes
      kernel32 = ctypes.windll.kernel32
      kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except Exception:
      # Fail silently on older Windows versions or permission issues
      pass

  def _is_color_terminal(self) -> bool:
    """Check if the current terminal supports colors."""
    import os

    # Check for explicit disable first
    if os.environ.get('NO_COLOR') or os.environ.get('CLICOLOR') == '0':
      return False
    elif os.environ.get('FORCE_COLOR') or os.environ.get('CLICOLOR'):
      # Check for explicit enable
      return True
    elif not sys.stdout.isatty():
      # Check if stdout is a TTY (not redirected to file/pipe)
      return False
    else:
      # Check environment variables that indicate color support
      term = sys.platform
      if term == 'win32':
        # Windows terminal color support
        return True
      else:
        # Unix-like systems
        term_env = os.environ.get('TERM', '').lower()
        if 'color' in term_env or term_env in ('xterm', 'xterm-256color', 'screen'):
          return True
        elif term_env in ('dumb', ''):
          # Default for dumb terminals or empty TERM
          return False
        else:
          return True

  def apply_style(self, text: str, style: ThemeStyle) -> str:
    """Apply a theme style to text.

    :param text: Text to style
    :param style: ThemeStyle configuration to apply
    :return: Styled text (or original text if colors disabled)
    """
    if not self.colors_enabled or not text:
      return text

    # Build color codes
    codes = []

    # Foreground color - handle RGB instances and ANSI strings
    if style.fg:
      if isinstance(style.fg, RGB):
        fg_code = style.fg.to_ansi(background=False)
        codes.append(fg_code)
      elif isinstance(style.fg, str) and style.fg.startswith('\x1b['):
        # Allow ANSI escape sequences as strings
        codes.append(style.fg)
      else:
        raise ValueError(f"Foreground color must be RGB instance or ANSI string, got {type(style.fg)}")

    # Background color - handle RGB instances and ANSI strings
    if style.bg:
      if isinstance(style.bg, RGB):
        bg_code = style.bg.to_ansi(background=True)
        codes.append(bg_code)
      elif isinstance(style.bg, str) and style.bg.startswith('\x1b['):
        # Allow ANSI escape sequences as strings
        codes.append(style.bg)
      else:
        raise ValueError(f"Background color must be RGB instance or ANSI string, got {type(style.bg)}")

    # Text styling (using defined ANSI constants)
    if style.bold:
      codes.append(Style.ANSI_BOLD.value)  # Use ANSI bold to avoid Style.BRIGHT color shifts
    if style.dim:
      codes.append(Style.DIM.value)  # ANSI DIM style
    if style.italic:
      codes.append(Style.ANSI_ITALIC.value)  # ANSI italic code (support varies by terminal)
    if style.underline:
      codes.append(Style.ANSI_UNDERLINE.value)  # ANSI underline code

    return ''.join(codes) + text + Style.RESET_ALL.value if codes else text

  def rgb_to_ansi256(self, r: int, g: int, b: int) -> int:
    """
    Convert RGB values to the closest ANSI 256-color code.

    Args:
        r, g, b: RGB values (0-255)

    Returns:
        ANSI color code (0-255)
    :deprecated: Use RGB._rgb_to_ansi256() method instead
    """
    # Use RGB class method for consistency
    rgb = RGB.from_ints(r, g, b)
    return rgb._rgb_to_ansi256(r, g, b)

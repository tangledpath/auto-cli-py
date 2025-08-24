"""Individual style configuration for text formatting."""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  pass


@dataclass
class ThemeStyle:
  """
  Individual style configuration for text formatting.
  Supports foreground/background colors (RGB instances only) and text decorations.
  """
  fg: 'RGB | None' = None  # Foreground color (RGB instance only)
  bg: 'RGB | None' = None  # Background color (RGB instance only)
  bold: bool = False  # Bold text
  italic: bool = False  # Italic text (may not work on all terminals)
  dim: bool = False  # Dimmed/faint text
  underline: bool = False  # Underlined text


@dataclass
class CommandStyleSection:
  """
  Hierarchical command styling configuration for a specific command level.
  Groups related styling attributes for commands and their options.
  """
  command_name: ThemeStyle  # Style for command names at this level
  command_description: ThemeStyle  # Style for command descriptions at this level
  option_name: ThemeStyle  # Style for option names at this level
  option_description: ThemeStyle  # Style for option descriptions at this level

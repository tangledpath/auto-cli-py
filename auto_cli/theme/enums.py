from enum import Enum


class Fore(Enum):
  """Foreground color constants."""
  BLACK = 0x000000
  RED = 0xFF0000
  GREEN = 0x008000
  YELLOW = 0xFFFF00
  BLUE = 0x0000FF
  MAGENTA = 0xFF00FF
  CYAN = 0x00FFFF
  WHITE = 0xFFFFFF

  # Bright colors
  LIGHTBLACK_EX = 0x808080
  LIGHTRED_EX = 0xFF8080
  LIGHTGREEN_EX = 0x80FF80
  LIGHTYELLOW_EX = 0xFFFF80
  LIGHTBLUE_EX = 0x8080FF
  LIGHTMAGENTA_EX = 0xFF80FF
  LIGHTCYAN_EX = 0x80FFFF
  LIGHTWHITE_EX = 0xF0F0F0


class Back(Enum):
  """Background color constants."""
  BLACK = 0x000000
  RED = 0xFF0000
  GREEN = 0x008000
  YELLOW = 0xFFFF00
  BLUE = 0x0000FF
  MAGENTA = 0xFF00FF
  CYAN = 0x00FFFF
  WHITE = 0xFFFFFF

  # Bright backgrounds
  LIGHTBLACK_EX = 0x808080
  LIGHTRED_EX = 0xFF8080
  LIGHTGREEN_EX = 0x80FF80
  LIGHTYELLOW_EX = 0xFFFF80
  LIGHTBLUE_EX = 0x8080FF
  LIGHTMAGENTA_EX = 0xFF80FF
  LIGHTCYAN_EX = 0x80FFFF
  LIGHTWHITE_EX = 0xF0F0F0


class Style(Enum):
  """Text style constants."""
  DIM = '\x1b[2m'
  RESET_ALL = '\x1b[0m'
  # All ANSI style codes in one place
  ANSI_BOLD = '\x1b[1m'  # Bold text
  ANSI_ITALIC = '\x1b[3m'  # Italic text (support varies by terminal)
  ANSI_UNDERLINE = '\x1b[4m'  # Underlined text


class ForeUniversal(Enum):
  """Universal foreground color palette with carefully curated colors."""

  # Blues
  BLUE = 0x2196F3  # Material Blue 500
  OKABE_BLUE = 0x0072B2  # Okabe-Ito Blue
  INDIGO = 0x3F51B5  # Material Indigo 500
  SKY_BLUE = 0x56B4E9  # Sky Blue

  # Greens
  BLUISH_GREEN = 0x009E73  # Bluish Green
  GREEN = 0x4CAF50  # Material Green 500
  DARK_GREEN = 0x08780D  # Dark green
  TEAL = 0x009688  # Material Teal 500

  # Orange/Yellow
  ORANGE = 0xE69F00  # Okabe-Ito Orange
  MATERIAL_ORANGE = 0xFF9800  # Material Orange 500
  GOLD = 0xF39C12  # Muted Gold

  # Red/Magenta
  VERMILION = 0xD55E00  # Okabe-Ito Vermilion
  REDDISH_PURPLE = 0xCC79A7  # Reddish Purple

  # Purple
  PURPLE = 0x9C27B0  # Material Purple 500
  DEEP_PURPLE = 0x673AB7  # Material Deep Purple 500

  # Neutrals
  BLUE_GREY = 0x607D8B  # Material Blue Grey 500
  DARK_BROWN = 0x604030  # Material Brown 500
  BROWN = 0x795548  # Material Brown 500
  MEDIUM_GREY = 0x757575  # Medium Grey
  IBM_GREY = 0x8D8D8D  # IBM Gray 50

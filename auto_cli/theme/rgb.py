"""Immutable RGB color class with comprehensive color operations."""
from __future__ import annotations

from enum import Enum
from typing import Tuple

from auto_cli.math_utils import MathUtils


class AdjustStrategy(Enum):
  """Strategy for color adjustment calculations."""
  LINEAR = "linear"
  COLOR_HSL = "color_hsl"
  MULTIPLICATIVE = "multiplicative"
  GAMMA = "gamma"
  LUMINANCE = "luminance"
  OVERLAY = "overlay"
  ABSOLUTE = "absolute"  # Legacy absolute adjustment


class RGB:
  """Immutable RGB color representation with values in range 0.0-1.0."""

  def __init__(self, r: float, g: float, b: float):
    """Initialize RGB with float values 0.0-1.0.

    :param r: Red component (0.0-1.0)
    :param g: Green component (0.0-1.0)
    :param b: Blue component (0.0-1.0)
    :raises ValueError: If any value is outside 0.0-1.0 range
    """
    if not (0.0 <= r <= 1.0):
      raise ValueError(f"Red component must be between 0.0 and 1.0, got {r}")
    if not (0.0 <= g <= 1.0):
      raise ValueError(f"Green component must be between 0.0 and 1.0, got {g}")
    if not (0.0 <= b <= 1.0):
      raise ValueError(f"Blue component must be between 0.0 and 1.0, got {b}")

    self._r = r
    self._g = g
    self._b = b

  @property
  def r(self) -> float:
    """Red component (0.0-1.0)."""
    return self._r

  @property
  def g(self) -> float:
    """Green component (0.0-1.0)."""
    return self._g

  @property
  def b(self) -> float:
    """Blue component (0.0-1.0)."""
    return self._b

  @classmethod
  def from_ints(cls, r: int, g: int, b: int) -> 'RGB':
    """Create RGB from integer values 0-255.

    :param r: Red component (0-255)
    :param g: Green component (0-255)
    :param b: Blue component (0-255)
    :return: RGB instance
    :raises ValueError: If any value is outside 0-255 range
    """
    if not (0 <= r <= 255):
      raise ValueError(f"Red component must be between 0 and 255, got {r}")
    if not (0 <= g <= 255):
      raise ValueError(f"Green component must be between 0 and 255, got {g}")
    if not (0 <= b <= 255):
      raise ValueError(f"Blue component must be between 0 and 255, got {b}")

    return cls(r / 255.0, g / 255.0, b / 255.0)

  @classmethod
  def from_rgb(cls, rgb: int) -> 'RGB':
    """Create RGB from hex integer (0x000000 to 0xFFFFFF).

    :param rgb: RGB value as integer (0x000000 to 0xFFFFFF)
    :return: RGB instance
    :raises ValueError: If value is outside valid range
    """
    if not (0 <= rgb <= 0xFFFFFF):
      raise ValueError(f"RGB value must be between 0 and 0xFFFFFF, got {rgb:06X}")

    # Extract RGB components from hex number
    r = (rgb >> 16) & 0xFF
    g = (rgb >> 8) & 0xFF
    b = rgb & 0xFF

    return cls.from_ints(r, g, b)

  def to_hex(self) -> str:
    """Convert to hex string format '#RRGGBB'.

    :return: Hex color string (e.g., '#FF5733')
    """
    r, g, b = self.to_ints()
    return f"#{r:02X}{g:02X}{b:02X}"

  def to_ints(self) -> Tuple[int, int, int]:
    """Convert to integer RGB tuple (0-255 range).

    :return: RGB tuple with integer values
    """
    return (int(self._r * 255), int(self._g * 255), int(self._b * 255))

  def to_ansi(self, background: bool = False) -> str:
    """Convert to ANSI escape code.

    :param background: Whether this is a background color
    :return: ANSI color code string
    """
    r, g, b = self.to_ints()
    ansi_code = self._rgb_to_ansi256(r, g, b)
    prefix = '\033[48;5;' if background else '\033[38;5;'
    return f"{prefix}{ansi_code}m"

  def adjust(self, *, brightness: float = 0.0, saturation: float = 0.0,
             strategy: AdjustStrategy = AdjustStrategy.LINEAR) -> 'RGB':
    """Adjust color using specified strategy."""
    # Handle strategies by their string values to support aliases
    if strategy.value == "linear":
      return self.linear_blend(brightness, saturation)
    elif strategy.value == "color_hsl":
      return self.hsl(brightness)
    elif strategy.value == "multiplicative":
      return self.multiplicative(brightness)
    elif strategy.value == "gamma":
      return self.gamma(brightness)
    elif strategy.value == "luminance":
      return self.luminance(brightness)
    elif strategy.value == "overlay":
      return self.overlay(brightness)
    elif strategy.value == "absolute":
      return self.absolute(brightness)
    else:
      return self

  def linear_blend(self, brightness: float = 0.0, saturation: float = 0.0) -> 'RGB':
    """Adjust color brightness and/or saturation, returning new RGB instance.

    :param brightness: Brightness adjustment (-5.0 to 5.0)
    :param saturation: Saturation adjustment (-5.0 to 5.0)
    :param strategy: Adjustment strategy
    :return: New RGB instance with adjustments applied
    :raises ValueError: If adjustment values are out of range
    """
    if not (-5.0 <= brightness <= 5.0):
      raise ValueError(f"Brightness must be between -5.0 and 5.0, got {brightness}")
    if not (-5.0 <= saturation <= 5.0):
      raise ValueError(f"Saturation must be between -5.0 and 5.0, got {saturation}")

    # Apply adjustments only if needed
    if brightness == 0.0 and saturation == 0.0:
      return self

    # Convert to integer for adjustment algorithm (matches existing behavior)
    r, g, b = self.to_ints()

    # Apply brightness adjustment (using existing algorithm from theme.py)
    # NOTE: The original algorithm has a bug where positive brightness makes colors darker
    # We maintain this behavior for backward compatibility
    if brightness != 0.0:
      factor = -brightness
      if brightness >= 0:
        # Original buggy behavior: negative factor makes colors darker
        r, g, b = [int(v + (255 - v) * factor) for v in (r, g, b)]
      else:
        # Darker - blend with black (0, 0, 0)
        factor = 1 + brightness  # brightness is negative, so this reduces values
        r, g, b = [int(v * factor) for v in (r, g, b)]

    # Clamp to valid range
    r, g, b = [int(MathUtils.clamp(v, 0, 255)) for v in (r, g, b)]

    # TODO: Add saturation adjustment when needed
    # For now, just brightness adjustment to match existing behavior

    return RGB.from_ints(r, g, b)

  def hsl(self, adjust_pct: float) -> 'RGB':
    """HSL method: Adjust lightness while preserving hue and saturation."""
    r, g, b = self.to_ints()
    h, s, l = self._rgb_to_hsl(r, g, b)

    # Adjust lightness
    l = l + (1.0 - l) * adjust_pct if adjust_pct >= 0 else l * (1 + adjust_pct)
    l = max(0.0, min(1.0, l))  # Clamp to valid range

    r_new, g_new, b_new = self._hsl_to_rgb(h, s, l)
    return RGB.from_ints(r_new, g_new, b_new)

  def multiplicative(self, adjust_pct: float) -> 'RGB':
    """Multiplicative method: Simple scaling of RGB values."""
    factor = 1.0 + adjust_pct
    r, g, b = self.to_ints()
    return RGB.from_ints(
      max(0, min(255, int(r * factor))),
      max(0, min(255, int(g * factor))),
      max(0, min(255, int(b * factor)))
    )

  def gamma(self, adjust_pct: float) -> 'RGB':
    """Gamma correction method: More perceptually uniform adjustments."""
    gamma = max(0.1, min(3.0, 1.0 - adjust_pct * 0.5))  # Convert to gamma value
    return RGB.from_ints(
      max(0, min(255, int(255 * pow(self._r, gamma)))),
      max(0, min(255, int(255 * pow(self._g, gamma)))),
      max(0, min(255, int(255 * pow(self._b, gamma))))
    )

  def luminance(self, adjust_pct: float) -> 'RGB':
    """Luminance-based method: Adjust based on perceived brightness."""
    r, g, b = self.to_ints()
    luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b  # ITU-R BT.709
    factor = 1.0 + adjust_pct * (255 - luminance) / 255 if adjust_pct >= 0 else 1.0 + adjust_pct
    return RGB.from_ints(
      max(0, min(255, int(r * factor))),
      max(0, min(255, int(g * factor))),
      max(0, min(255, int(b * factor)))
    )

  def overlay(self, adjust_pct: float) -> 'RGB':
    """Overlay blend mode: Similar to Photoshop's overlay effect."""

    def overlay_blend(base: float, overlay: float) -> float:
      """Apply overlay blend formula."""
      return 2 * base * overlay if base < 0.5 else 1 - 2 * (1 - base) * (1 - overlay)

    overlay_val = 0.5 + adjust_pct * 0.5  # Maps to 0.0-1.0 range
    return RGB.from_ints(
      max(0, min(255, int(255 * overlay_blend(self._r, overlay_val)))),
      max(0, min(255, int(255 * overlay_blend(self._g, overlay_val)))),
      max(0, min(255, int(255 * overlay_blend(self._b, overlay_val))))
    )

  def absolute(self, adjust_pct: float) -> 'RGB':
    """Absolute adjustment method: Legacy absolute color adjustment."""
    r, g, b = self.to_ints()
    # Legacy behavior: color + (255 - color) * (-adjust_pct)
    factor = -adjust_pct
    return RGB.from_ints(
      max(0, min(255, int(r + (255 - r) * factor))),
      max(0, min(255, int(g + (255 - g) * factor))),
      max(0, min(255, int(b + (255 - b) * factor)))
    )

  @staticmethod
  def _rgb_to_hsl(r: int, g: int, b: int) -> Tuple[float, float, float]:
    """Convert RGB to HSL color space."""
    r_norm, g_norm, b_norm = r / 255.0, g / 255.0, b / 255.0

    max_val = max(r_norm, g_norm, b_norm)
    min_val = min(r_norm, g_norm, b_norm)
    diff = max_val - min_val

    # Lightness
    l = (max_val + min_val) / 2.0

    if diff == 0:
      h = s = 0  # Achromatic
    else:
      # Saturation
      s = diff / (2 - max_val - min_val) if l > 0.5 else diff / (max_val + min_val)

      # Hue
      if max_val == r_norm:
        h = (g_norm - b_norm) / diff + (6 if g_norm < b_norm else 0)
      elif max_val == g_norm:
        h = (b_norm - r_norm) / diff + 2
      else:
        h = (r_norm - g_norm) / diff + 4
      h /= 6

    return h, s, l

  @staticmethod
  def _hsl_to_rgb(h: float, s: float, l: float) -> Tuple[int, int, int]:
    """Convert HSL to RGB color space."""

    def hue_to_rgb(p: float, q: float, t: float) -> float:
      """Convert hue to RGB component."""
      t = t + 1 if t < 0 else t - 1 if t > 1 else t
      if t < 1 / 6:
        result = p + (q - p) * 6 * t
      elif t < 1 / 2:
        result = q
      elif t < 2 / 3:
        result = p + (q - p) * (2 / 3 - t) * 6
      else:
        result = p
      return result

    if s == 0:
      r = g = b = l  # Achromatic
    else:
      q = l * (1 + s) if l < 0.5 else l + s - l * s
      p = 2 * l - q
      r = hue_to_rgb(p, q, h + 1 / 3)
      g = hue_to_rgb(p, q, h)
      b = hue_to_rgb(p, q, h - 1 / 3)

    return int(r * 255), int(g * 255), int(b * 255)

  def _rgb_to_ansi256(self, r: int, g: int, b: int) -> int:
    """Convert RGB values to the closest ANSI 256-color code.

    :param r: Red component (0-255)
    :param g: Green component (0-255)
    :param b: Blue component (0-255)
    :return: ANSI color code (0-255)
    """
    # Check if it's close to grayscale (colors 232-255)
    if abs(r - g) < 10 and abs(g - b) < 10 and abs(r - b) < 10:
      # Use grayscale palette (24 shades)
      gray = (r + g + b) // 3
      # Map to grayscale range
      return 16 if gray < 8 else 231 if gray > 238 else 232 + (gray - 8) * 23 // 230

    # Use 6x6x6 color cube (colors 16-231)
    # Map RGB values to 6-level scale (0-5)
    r6 = min(5, r * 6 // 256)
    g6 = min(5, g * 6 // 256)
    b6 = min(5, b * 6 // 256)

    return 16 + (36 * r6) + (6 * g6) + b6

  def __eq__(self, other) -> bool:
    """Check equality with another RGB instance."""
    return isinstance(other, RGB) and self._r == other._r and self._g == other._g and self._b == other._b

  def __hash__(self) -> int:
    """Make RGB hashable."""
    return hash((self._r, self._g, self._b))

  def __repr__(self) -> str:
    """String representation for debugging."""
    return f"RGB(r={self._r:.3f}, g={self._g:.3f}, b={self._b:.3f})"

  def __str__(self) -> str:
    """User-friendly string representation."""
    return self.to_hex()

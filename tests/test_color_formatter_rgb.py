"""Test ColorFormatter with RGB instances."""
import pytest

from auto_cli.theme.color_formatter import ColorFormatter
from auto_cli.theme.rgb import RGB
from auto_cli.theme.theme_style import ThemeStyle


class TestColorFormatterRGB:
  """Test ColorFormatter with RGB instances."""

  def test_apply_style_with_rgb_foreground(self):
    """Test apply_style with RGB foreground color."""
    formatter = ColorFormatter(enable_colors=True)
    rgb_color = RGB.from_rgb(0xFF5733)
    style = ThemeStyle(fg=rgb_color)

    result = formatter.apply_style("test", style)

    # Should contain ANSI escape codes
    assert "\033[38;5;" in result  # Foreground color code
    assert "test" in result
    assert "\033[0m" in result  # Reset code

  def test_apply_style_with_rgb_background(self):
    """Test apply_style with RGB background color."""
    formatter = ColorFormatter(enable_colors=True)
    rgb_color = RGB.from_rgb(0x00FF00)
    style = ThemeStyle(bg=rgb_color)

    result = formatter.apply_style("test", style)

    # Should contain ANSI escape codes for background
    assert "\033[48;5;" in result  # Background color code
    assert "test" in result
    assert "\033[0m" in result  # Reset code

  def test_apply_style_with_rgb_both_colors(self):
    """Test apply_style with RGB foreground and background colors."""
    formatter = ColorFormatter(enable_colors=True)
    fg_color = RGB.from_rgb(0xFF5733)
    bg_color = RGB.from_rgb(0x00FF00)
    style = ThemeStyle(fg=fg_color, bg=bg_color, bold=True)

    result = formatter.apply_style("test", style)

    # Should contain both foreground and background codes
    assert "\033[38;5;" in result  # Foreground color code
    assert "\033[48;5;" in result  # Background color code
    assert "\033[1m" in result  # Bold code
    assert "test" in result
    assert "\033[0m" in result  # Reset code

  def test_apply_style_rgb_consistency(self):
    """Test that equivalent RGB instances produce same output."""
    formatter = ColorFormatter(enable_colors=True)
    rgb_color1 = RGB.from_rgb(0xFF5733)
    r, g, b = rgb_color1.to_ints()
    rgb_color2 = RGB.from_ints(r, g, b)  # Equivalent RGB from ints

    style1 = ThemeStyle(fg=rgb_color1)
    style2 = ThemeStyle(fg=rgb_color2)

    result1 = formatter.apply_style("test", style1)
    result2 = formatter.apply_style("test", style2)

    # Results should be identical
    assert result1 == result2

  def test_apply_style_colors_disabled(self):
    """Test apply_style with colors disabled."""
    formatter = ColorFormatter(enable_colors=False)
    rgb_color = RGB.from_rgb(0xFF5733)
    style = ThemeStyle(fg=rgb_color, bold=True)

    result = formatter.apply_style("test", style)

    # Should return plain text when colors are disabled
    assert result == "test"
    assert "\033[" not in result  # No ANSI codes

  def test_apply_style_invalid_fg_type(self):
    """Test apply_style with invalid foreground color type."""
    formatter = ColorFormatter(enable_colors=True)
    style = ThemeStyle(fg=123)  # Invalid type

    with pytest.raises(ValueError, match="Foreground color must be RGB instance or ANSI string"):
      formatter.apply_style("test", style)

  def test_apply_style_invalid_bg_type(self):
    """Test apply_style with invalid background color type."""
    formatter = ColorFormatter(enable_colors=True)
    style = ThemeStyle(bg=123)  # Invalid type

    with pytest.raises(ValueError, match="Background color must be RGB instance or ANSI string"):
      formatter.apply_style("test", style)

  def test_apply_style_with_all_text_styles(self):
    """Test apply_style with RGB color and all text styles."""
    formatter = ColorFormatter(enable_colors=True)
    rgb_color = RGB.from_rgb(0xFF5733)
    style = ThemeStyle(
      fg=rgb_color,
      bold=True,
      italic=True,
      dim=True,
      underline=True
    )

    result = formatter.apply_style("test", style)

    # Should contain all style codes
    assert "\033[38;5;" in result  # Foreground color
    assert "\033[1m" in result  # Bold
    assert "\033[3m" in result  # Italic
    assert "\033[2m" in result  # Dim
    assert "\033[4m" in result  # Underline
    assert "test" in result
    assert "\033[0m" in result  # Reset

  def test_rgb_to_ansi256_delegation(self):
    """Test that rgb_to_ansi256 properly delegates to RGB class."""
    formatter = ColorFormatter(enable_colors=True)

    result = formatter.rgb_to_ansi256(255, 87, 51)

    # Should delegate to RGB class
    rgb = RGB.from_ints(255, 87, 51)
    expected = rgb._rgb_to_ansi256(255, 87, 51)
    assert result == expected

  def test_mixed_rgb_and_string_styles(self):
    """Test theme with mixed RGB instances and string colors."""
    formatter = ColorFormatter(enable_colors=True)

    # RGB foreground, string background (ANSI code)
    rgb_fg = RGB.from_rgb(0xFF5733)
    ansi_bg = "\033[48;5;46m"  # Direct ANSI code
    style = ThemeStyle(fg=rgb_fg, bg=ansi_bg)

    result = formatter.apply_style("test", style)

    # Should handle both types properly
    assert "\033[38;5;" in result  # RGB foreground
    assert ansi_bg in result  # String background
    assert "test" in result
    assert "\033[0m" in result  # Reset

  def test_empty_text(self):
    """Test apply_style with empty text."""
    formatter = ColorFormatter(enable_colors=True)
    rgb_color = RGB.from_rgb(0xFF5733)
    style = ThemeStyle(fg=rgb_color)

    result = formatter.apply_style("", style)

    # Empty text should return empty string
    assert result == ""

  def test_none_text(self):
    """Test apply_style with None text."""
    formatter = ColorFormatter(enable_colors=True)
    rgb_color = RGB.from_rgb(0xFF5733)
    style = ThemeStyle(fg=rgb_color)

    result = formatter.apply_style(None, style)

    # None text should return None
    assert result is None

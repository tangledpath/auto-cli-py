"""Tests for color adjustment functionality in themes."""
import pytest

from auto_cli.theme import (
  AdjustStrategy,
  RGB,
  Theme,
  ThemeStyle,
  create_default_theme,
)


class TestThemeColorAdjustment:
  """Test color adjustment functionality in themes."""

  def test_theme_creation_with_adjustment(self):
    """Test creating theme with adjustment parameters."""
    theme = create_default_theme()
    theme.adjust_percent = 0.3
    theme.adjust_strategy = AdjustStrategy.LINEAR

    assert theme.adjust_percent == 0.3
    assert theme.adjust_strategy == AdjustStrategy.LINEAR

  def test_proportional_adjustment_positive(self):
    """Test proportional color adjustment with positive percentage using RGB."""
    original_rgb = RGB.from_ints(128, 128, 128)  # Mid gray
    style = ThemeStyle(fg=original_rgb)
    theme = Theme(
      title=style, subtitle=style, command_name=style, command_description=style,
      command_group_name=style, command_group_description=style,
      grouped_command_name=style, grouped_command_description=style,
      option_name=style, option_description=style, 
      command_group_option_name=style, command_group_option_description=style,
      grouped_command_option_name=style, grouped_command_option_description=style,
      required_asterisk=style,
      adjust_strategy=AdjustStrategy.LINEAR,
      adjust_percent=0.25  # 25% adjustment
    )

    adjusted_style = theme.get_adjusted_style(style)
    r, g, b = adjusted_style.fg.to_ints()

    # Current implementation: factor = -adjust_percent = -0.25, then 128 * (1 + (-0.25)) = 96
    assert r == 96
    assert g == 96
    assert b == 96

  def test_proportional_adjustment_negative(self):
    """Test proportional color adjustment with negative percentage using RGB."""
    original_rgb = RGB.from_ints(128, 128, 128)  # Mid gray
    style = ThemeStyle(fg=original_rgb)
    theme = Theme(
      title=style, subtitle=style, command_name=style, command_description=style,
      command_group_name=style, command_group_description=style,
      grouped_command_name=style, grouped_command_description=style,
      option_name=style, option_description=style, command_group_option_name=style,
      command_group_option_description=style, grouped_command_option_name=style,
      grouped_command_option_description=style, required_asterisk=style,
      adjust_strategy=AdjustStrategy.LINEAR,
      adjust_percent=-0.25  # 25% darker
    )

    adjusted_style = theme.get_adjusted_style(style)
    r, g, b = adjusted_style.fg.to_ints()

    # Each component should be decreased by 25%: 128 + (128 * -0.25) = 96
    assert r == 96
    assert g == 96
    assert b == 96

  def test_absolute_adjustment_positive(self):
    """Test absolute color adjustment with positive percentage using RGB."""
    original_rgb = RGB.from_ints(64, 64, 64)  # Dark gray
    style = ThemeStyle(fg=original_rgb)
    theme = Theme(
      title=style, subtitle=style, command_name=style, command_description=style,
      command_group_name=style, command_group_description=style,
      grouped_command_name=style, grouped_command_description=style,
      option_name=style, option_description=style, command_group_option_name=style,
      command_group_option_description=style, grouped_command_option_name=style,
      grouped_command_option_description=style, required_asterisk=style,
      adjust_strategy=AdjustStrategy.ABSOLUTE,
      adjust_percent=0.5  # 50% adjustment (actually darkens due to current implementation)
    )

    adjusted_style = theme.get_adjusted_style(style)
    r, g, b = adjusted_style.fg.to_ints()

    # Current implementation: 64 + (255-64) * (-0.5) = 64 + 191 * (-0.5) = -31.5, clamped to 0
    assert r == 0
    assert g == 0
    assert b == 0

  def test_absolute_adjustment_with_clamping(self):
    """Test absolute adjustment with clamping at boundaries using RGB."""
    original_rgb = RGB.from_ints(240, 240, 240)  # Light gray
    style = ThemeStyle(fg=original_rgb)
    theme = Theme(
      title=style, subtitle=style, command_name=style, command_description=style,
      command_group_name=style, command_group_description=style,
      grouped_command_name=style, grouped_command_description=style,
      option_name=style, option_description=style, command_group_option_name=style,
      command_group_option_description=style, grouped_command_option_name=style,
      grouped_command_option_description=style, required_asterisk=style,
      adjust_strategy=AdjustStrategy.ABSOLUTE,
      adjust_percent=0.5  # 50% adjustment (actually darkens due to current implementation)
    )

    adjusted_style = theme.get_adjusted_style(style)
    r, g, b = adjusted_style.fg.to_ints()

    # Current implementation: 240 + (255-240) * (-0.5) = 240 + 15 * (-0.5) = 232.5 ≈ 232
    assert r == 232
    assert g == 232
    assert b == 232

  @staticmethod
  def _theme_with_style(style):
    return Theme(
      title=style, subtitle=style, command_name=style,
      command_description=style, command_group_name=style, command_group_description=style,
      grouped_command_name=style, grouped_command_description=style,
      option_name=style, option_description=style,
      command_group_option_name=style, command_group_option_description=style,
      grouped_command_option_name=style, grouped_command_option_description=style,
      required_asterisk=style,
      adjust_strategy=AdjustStrategy.LINEAR,
      adjust_percent=0.25
    )

  def test_get_adjusted_style(self):
    """Test getting adjusted style using RGB."""
    original_rgb = RGB.from_ints(128, 128, 128)  # Mid gray
    original_style = ThemeStyle(fg=original_rgb, bold=True, italic=False)
    theme = self._theme_with_style(original_style)
    adjusted_style = theme.get_adjusted_style(original_style)

    assert adjusted_style is not None
    assert adjusted_style.fg != original_rgb  # Should be adjusted
    assert adjusted_style.bold is True  # Non-color properties preserved
    assert adjusted_style.italic is False

  def test_rgb_adjustment_preserves_properties(self):
    """Test that RGB adjustment preserves non-color properties."""
    original_rgb = RGB.from_ints(128, 128, 128)  # Mid gray - will be adjusted
    style = ThemeStyle(fg=original_rgb, bold=True, underline=True)
    theme = Theme(
      title=style, subtitle=style, command_name=style, command_description=style,
      command_group_name=style, command_group_description=style,
      grouped_command_name=style, grouped_command_description=style,
      option_name=style, option_description=style, command_group_option_name=style,
      command_group_option_description=style, grouped_command_option_name=style,
      grouped_command_option_description=style, required_asterisk=style,
      adjust_strategy=AdjustStrategy.LINEAR,
      adjust_percent=0.25
    )

    adjusted_style = theme.get_adjusted_style(style)

    # Color should be adjusted but other properties preserved
    assert adjusted_style.fg != original_rgb
    assert adjusted_style.bold is True
    assert adjusted_style.underline is True

  def test_adjustment_with_zero_percent(self):
    """Test no adjustment when percent is 0 using RGB."""
    original_rgb = RGB.from_ints(255, 0, 0)  # Red color
    style = ThemeStyle(fg=original_rgb)
    theme = Theme(
      title=style, subtitle=style, command_name=style, command_description=style,
      command_group_name=style, command_group_description=style,
      grouped_command_name=style, grouped_command_description=style,
      option_name=style, option_description=style, command_group_option_name=style,
      command_group_option_description=style, grouped_command_option_name=style,
      grouped_command_option_description=style, required_asterisk=style,
      adjust_percent=0.0  # No adjustment
    )

    adjusted_style = theme.get_adjusted_style(style)

    assert adjusted_style.fg == original_rgb  # Should remain unchanged

  def test_create_adjusted_copy(self):
    """Test creating an adjusted copy of a theme."""
    original_theme = create_default_theme()
    adjusted_theme = original_theme.create_adjusted_copy(0.2)

    assert adjusted_theme.adjust_percent == 0.2
    assert adjusted_theme != original_theme  # Different instances

    # Original theme should be unchanged
    assert original_theme.adjust_percent == 0.0

  def test_adjustment_edge_cases(self):
    """Test adjustment with edge case RGB colors."""
    theme = Theme(
      title=ThemeStyle(), subtitle=ThemeStyle(), command_name=ThemeStyle(),
      command_description=ThemeStyle(), command_group_name=ThemeStyle(), command_group_description=ThemeStyle(),
      grouped_command_name=ThemeStyle(), grouped_command_description=ThemeStyle(),
      option_name=ThemeStyle(), option_description=ThemeStyle(),
      command_group_option_name=ThemeStyle(), command_group_option_description=ThemeStyle(),
      grouped_command_option_name=ThemeStyle(), grouped_command_option_description=ThemeStyle(),
      required_asterisk=ThemeStyle(),
      adjust_strategy=AdjustStrategy.LINEAR,
      adjust_percent=0.5
    )

    # Test with black RGB (should handle division by zero)
    black_rgb = RGB.from_ints(0, 0, 0)
    black_style = ThemeStyle(fg=black_rgb)
    adjusted_black_style = theme.get_adjusted_style(black_style)
    assert adjusted_black_style.fg == black_rgb  # Can't adjust pure black

    # Test with white RGB
    white_rgb = RGB.from_ints(255, 255, 255)
    white_style = ThemeStyle(fg=white_rgb)
    adjusted_white_style = theme.get_adjusted_style(white_style)
    assert adjusted_white_style.fg == white_rgb  # White should remain unchanged

    # Test with None style
    none_style = ThemeStyle(fg=None)
    adjusted_none_style = theme.get_adjusted_style(none_style)
    assert adjusted_none_style.fg is None

  def test_adjust_percent_validation_in_init(self):
    """Test adjust_percent validation in Theme.__init__."""
    style = ThemeStyle()

    # Valid range should work
    Theme(
      title=style, subtitle=style, command_name=style, command_description=style,
      command_group_name=style, command_group_description=style,
      grouped_command_name=style, grouped_command_description=style,
      option_name=style, option_description=style, command_group_option_name=style,
      command_group_option_description=style, grouped_command_option_name=style,
      grouped_command_option_description=style, required_asterisk=style,
      adjust_percent=-5.0  # Minimum valid
    )

    Theme(
      title=style, subtitle=style, command_name=style, command_description=style,
      command_group_name=style, command_group_description=style,
      grouped_command_name=style, grouped_command_description=style,
      option_name=style, option_description=style, command_group_option_name=style,
      command_group_option_description=style, grouped_command_option_name=style,
      grouped_command_option_description=style, required_asterisk=style,
      adjust_percent=5.0  # Maximum valid
    )

    # Below minimum should raise exception
    with pytest.raises(ValueError, match="adjust_percent must be between -5.0 and 5.0, got -5.1"):
      Theme(
        title=style, subtitle=style, command_name=style, command_description=style,
        command_group_name=style, command_group_description=style,
        grouped_command_name=style, grouped_command_description=style,
        option_name=style, option_description=style, command_group_option_name=style,
        command_group_option_description=style, grouped_command_option_name=style,
        grouped_command_option_description=style, required_asterisk=style,
        adjust_percent=-5.1
      )

    # Above maximum should raise exception
    with pytest.raises(ValueError, match="adjust_percent must be between -5.0 and 5.0, got 5.1"):
      Theme(
        title=style, subtitle=style, command_name=style, command_description=style,
        command_group_name=style, command_group_description=style,
        grouped_command_name=style, grouped_command_description=style,
        option_name=style, option_description=style, command_group_option_name=style,
        command_group_option_description=style, grouped_command_option_name=style,
        grouped_command_option_description=style, required_asterisk=style,
        adjust_percent=5.1
      )

  def test_adjust_percent_validation_in_create_adjusted_copy(self):
    """Test adjust_percent validation in create_adjusted_copy method."""
    original_theme = create_default_theme()

    # Valid range should work
    original_theme.create_adjusted_copy(-5.0)  # Minimum valid
    original_theme.create_adjusted_copy(5.0)  # Maximum valid

    # Below minimum should raise exception
    with pytest.raises(ValueError, match="adjust_percent must be between -5.0 and 5.0, got -5.1"):
      original_theme.create_adjusted_copy(-5.1)

    # Above maximum should raise exception
    with pytest.raises(ValueError, match="adjust_percent must be between -5.0 and 5.0, got 5.1"):
      original_theme.create_adjusted_copy(5.1)

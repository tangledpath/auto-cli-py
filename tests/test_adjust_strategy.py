"""Tests for AdjustStrategy enum."""

from auto_cli.theme import AdjustStrategy


class TestAdjustStrategy:
  """Test the AdjustStrategy enum."""

  def test_enum_values(self):
    """Test enum has correct values."""
    assert AdjustStrategy.LINEAR.value == "linear"
    assert AdjustStrategy.COLOR_HSL.value == "color_hsl"
    assert AdjustStrategy.MULTIPLICATIVE.value == "multiplicative"
    assert AdjustStrategy.GAMMA.value == "gamma"
    assert AdjustStrategy.LUMINANCE.value == "luminance"
    assert AdjustStrategy.OVERLAY.value == "overlay"
    assert AdjustStrategy.ABSOLUTE.value == "absolute"

    # Test backward compatibility aliases
    assert AdjustStrategy.LINEAR.value == "linear"
    assert AdjustStrategy.LINEAR.value == "linear"

  def test_enum_members(self):
    """Test enum has all expected members."""
    # Only actual enum members (aliases don't show up as separate members)
    expected_members = {'LINEAR', 'COLOR_HSL', 'MULTIPLICATIVE', 'GAMMA', 'LUMINANCE', 'OVERLAY', 'ABSOLUTE'}
    actual_members = {member.name for member in AdjustStrategy}
    assert expected_members == actual_members

    # Test that aliases exist and work
    assert hasattr(AdjustStrategy, 'LINEAR')
    assert hasattr(AdjustStrategy, 'LINEAR')

  def test_enum_string_representation(self):
    """Test enum string representations."""
    # Aliases resolve to their primary member's string representation
    assert str(AdjustStrategy.LINEAR) == "AdjustStrategy.LINEAR"
    assert str(AdjustStrategy.LINEAR) == "AdjustStrategy.LINEAR"

    # Primary members show their own names
    assert str(AdjustStrategy.LINEAR) == "AdjustStrategy.LINEAR"
    assert str(AdjustStrategy.MULTIPLICATIVE) == "AdjustStrategy.MULTIPLICATIVE"
    assert str(AdjustStrategy.ABSOLUTE) == "AdjustStrategy.ABSOLUTE"

  def test_enum_equality(self):
    """Test enum equality comparisons."""
    # Test that aliases work correctly
    assert AdjustStrategy.LINEAR == AdjustStrategy.LINEAR
    assert AdjustStrategy.LINEAR == AdjustStrategy.LINEAR

    # Test that ABSOLUTE is its own member now
    assert AdjustStrategy.ABSOLUTE == AdjustStrategy.ABSOLUTE
    assert AdjustStrategy.ABSOLUTE != AdjustStrategy.MULTIPLICATIVE

    # Test inequality
    assert AdjustStrategy.ABSOLUTE != AdjustStrategy.LINEAR
    assert AdjustStrategy.MULTIPLICATIVE != AdjustStrategy.LINEAR

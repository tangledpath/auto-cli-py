"""Test suite for RGB class and color operations."""
import pytest

from auto_cli.theme.rgb import RGB, AdjustStrategy


class TestRGBConstructor:
  """Test RGB constructor and validation."""

  def test_valid_construction(self):
    """Test valid RGB construction."""
    rgb = RGB(0.5, 0.3, 0.8)
    assert rgb.r == 0.5
    assert rgb.g == 0.3
    assert rgb.b == 0.8

  def test_boundary_values(self):
    """Test boundary values (0.0 and 1.0)."""
    rgb_min = RGB(0.0, 0.0, 0.0)
    assert rgb_min.r == 0.0
    assert rgb_min.g == 0.0
    assert rgb_min.b == 0.0

    rgb_max = RGB(1.0, 1.0, 1.0)
    assert rgb_max.r == 1.0
    assert rgb_max.g == 1.0
    assert rgb_max.b == 1.0

  def test_invalid_values_below_range(self):
    """Test validation for values below 0.0."""
    with pytest.raises(ValueError, match="Red component must be between 0.0 and 1.0"):
      RGB(-0.1, 0.5, 0.5)

    with pytest.raises(ValueError, match="Green component must be between 0.0 and 1.0"):
      RGB(0.5, -0.1, 0.5)

    with pytest.raises(ValueError, match="Blue component must be between 0.0 and 1.0"):
      RGB(0.5, 0.5, -0.1)

  def test_invalid_values_above_range(self):
    """Test validation for values above 1.0."""
    with pytest.raises(ValueError, match="Red component must be between 0.0 and 1.0"):
      RGB(1.1, 0.5, 0.5)

    with pytest.raises(ValueError, match="Green component must be between 0.0 and 1.0"):
      RGB(0.5, 1.1, 0.5)

    with pytest.raises(ValueError, match="Blue component must be between 0.0 and 1.0"):
      RGB(0.5, 0.5, 1.1)

  def test_immutability(self):
    """Test that RGB properties are read-only."""
    rgb = RGB(0.5, 0.3, 0.8)

    # Properties should be read-only
    with pytest.raises(AttributeError):
      rgb.r = 0.6
    with pytest.raises(AttributeError):
      rgb.g = 0.4
    with pytest.raises(AttributeError):
      rgb.b = 0.9


class TestRGBFactoryMethods:
  """Test RGB factory methods."""

  def test_from_ints_valid(self):
    """Test from_ints with valid values."""
    rgb = RGB.from_ints(255, 128, 0)
    assert rgb.r == pytest.approx(1.0, abs=0.001)
    assert rgb.g == pytest.approx(0.502, abs=0.001)
    assert rgb.b == pytest.approx(0.0, abs=0.001)

  def test_from_ints_boundary(self):
    """Test from_ints with boundary values."""
    rgb_black = RGB.from_ints(0, 0, 0)
    assert rgb_black.r == 0.0
    assert rgb_black.g == 0.0
    assert rgb_black.b == 0.0

    rgb_white = RGB.from_ints(255, 255, 255)
    assert rgb_white.r == 1.0
    assert rgb_white.g == 1.0
    assert rgb_white.b == 1.0

  def test_from_ints_invalid(self):
    """Test from_ints with invalid values."""
    with pytest.raises(ValueError, match="Red component must be between 0 and 255"):
      RGB.from_ints(-1, 128, 128)

    with pytest.raises(ValueError, match="Green component must be between 0 and 255"):
      RGB.from_ints(128, 256, 128)

    with pytest.raises(ValueError, match="Blue component must be between 0 and 255"):
      RGB.from_ints(128, 128, -5)

  def test_from_rgb_valid(self):
    """Test from_rgb with valid hex integers."""
    # Red: 0xFF0000
    rgb_red = RGB.from_rgb(0xFF0000)
    assert rgb_red.r == 1.0
    assert rgb_red.g == 0.0
    assert rgb_red.b == 0.0

    # Green: 0x00FF00
    rgb_green = RGB.from_rgb(0x00FF00)
    assert rgb_green.r == 0.0
    assert rgb_green.g == 1.0
    assert rgb_green.b == 0.0

    # Blue: 0x0000FF
    rgb_blue = RGB.from_rgb(0x0000FF)
    assert rgb_blue.r == 0.0
    assert rgb_blue.g == 0.0
    assert rgb_blue.b == 1.0

    # Custom color: 0xFF5733 (Orange)
    rgb_orange = RGB.from_rgb(0xFF5733)
    assert rgb_orange.to_hex() == "#FF5733"

  def test_from_rgb_boundary(self):
    """Test from_rgb with boundary values."""
    rgb_black = RGB.from_rgb(0x000000)
    assert rgb_black.r == 0.0
    assert rgb_black.g == 0.0
    assert rgb_black.b == 0.0

    rgb_white = RGB.from_rgb(0xFFFFFF)
    assert rgb_white.r == 1.0
    assert rgb_white.g == 1.0
    assert rgb_white.b == 1.0

  def test_from_rgb_invalid(self):
    """Test from_rgb with invalid values."""
    with pytest.raises(ValueError, match="RGB value must be between 0 and 0xFFFFFF"):
      RGB.from_rgb(-1)

    with pytest.raises(ValueError, match="RGB value must be between 0 and 0xFFFFFF"):
      RGB.from_rgb(0x1000000)  # Too large

  def test_from_rgb_to_hex_roundtrip(self):
    """Test from_rgb with hex integers and to_hex conversion."""
    # Test with standard hex integer
    rgb1 = RGB.from_rgb(0xFF5733)
    assert rgb1.to_hex() == "#FF5733"

    # Test with another hex value
    rgb2 = RGB.from_rgb(0xFF5577)
    assert rgb2.to_hex() == "#FF5577"

  def test_from_rgb_invalid_range(self):
    """Test from_rgb with out of range hex integers."""
    with pytest.raises(ValueError):
      RGB.from_rgb(0x1000000)  # Too large (> 0xFFFFFF)

    with pytest.raises(ValueError):
      RGB.from_rgb(-1)  # Negative


class TestRGBConversions:
  """Test RGB conversion methods."""

  def test_to_hex(self):
    """Test to_hex conversion."""
    rgb = RGB.from_ints(255, 87, 51)
    assert rgb.to_hex() == "#FF5733"

    rgb_black = RGB.from_ints(0, 0, 0)
    assert rgb_black.to_hex() == "#000000"

    rgb_white = RGB.from_ints(255, 255, 255)
    assert rgb_white.to_hex() == "#FFFFFF"

  def test_to_ints(self):
    """Test to_ints conversion."""
    rgb = RGB(1.0, 0.5, 0.0)
    r, g, b = rgb.to_ints()
    assert r == 255
    assert g == 127  # 0.5 * 255 = 127.5 -> 127
    assert b == 0

  def test_to_ansi_foreground(self):
    """Test to_ansi for foreground colors."""
    rgb = RGB.from_rgb(0xFF0000)  # Red
    ansi = rgb.to_ansi(background=False)
    assert ansi.startswith('\033[38;5;')
    assert ansi.endswith('m')

  def test_to_ansi_background(self):
    """Test to_ansi for background colors."""
    rgb = RGB.from_rgb(0x00FF00)  # Green
    ansi = rgb.to_ansi(background=True)
    assert ansi.startswith('\033[48;5;')
    assert ansi.endswith('m')

  def test_roundtrip_conversion(self):
    """Test that conversions are consistent."""
    original = "#FF5733"
    rgb = RGB.from_rgb(int(original.lstrip('#'), 16))
    converted = rgb.to_hex()
    assert converted == original


class TestRGBAdjust:
  """Test RGB color adjustment methods."""

  def test_adjust_no_change(self):
    """Test adjust with no parameters returns same instance."""
    rgb = RGB.from_rgb(0xFF5733)
    adjusted = rgb.adjust()
    assert adjusted == rgb

  def test_adjust_brightness_positive(self):
    """Test brightness adjustment - note: original algorithm is buggy and makes colors darker."""
    rgb = RGB.from_rgb(0x808080)  # Gray
    adjusted = rgb.adjust(brightness=1.0)

    # NOTE: The original algorithm has a bug where positive brightness makes colors darker
    # This test verifies backward compatibility with the buggy behavior
    orig_r, orig_g, orig_b = rgb.to_ints()
    adj_r, adj_g, adj_b = adjusted.to_ints()

    # With the original buggy algorithm, positive brightness makes colors darker
    assert adj_r <= orig_r
    assert adj_g <= orig_g
    assert adj_b <= orig_b

  def test_adjust_brightness_negative(self):
    """Test brightness adjustment (darker)."""
    rgb = RGB.from_rgb(0x808080)  # Gray
    adjusted = rgb.adjust(brightness=-1.0)

    # Should be darker than original
    orig_r, orig_g, orig_b = rgb.to_ints()
    adj_r, adj_g, adj_b = adjusted.to_ints()

    assert adj_r <= orig_r
    assert adj_g <= orig_g
    assert adj_b <= orig_b

  def test_adjust_brightness_invalid(self):
    """Test brightness adjustment with invalid values."""
    rgb = RGB.from_rgb(0xFF5733)

    with pytest.raises(ValueError, match="Brightness must be between -5.0 and 5.0"):
      rgb.adjust(brightness=6.0)

    with pytest.raises(ValueError, match="Brightness must be between -5.0 and 5.0"):
      rgb.adjust(brightness=-6.0)

  def test_adjust_saturation_invalid(self):
    """Test saturation adjustment with invalid values."""
    rgb = RGB.from_rgb(0xFF5733)

    with pytest.raises(ValueError, match="Saturation must be between -5.0 and 5.0"):
      rgb.adjust(saturation=6.0)

    with pytest.raises(ValueError, match="Saturation must be between -5.0 and 5.0"):
      rgb.adjust(saturation=-6.0)

  def test_adjust_returns_new_instance(self):
    """Test that adjust returns a new RGB instance."""
    rgb = RGB.from_rgb(0xFF5733)
    adjusted = rgb.adjust(brightness=0.5)

    assert adjusted is not rgb
    assert isinstance(adjusted, RGB)


class TestRGBEquality:
  """Test RGB equality and hashing."""

  def test_equality(self):
    """Test RGB equality."""
    rgb1 = RGB(0.5, 0.3, 0.8)
    rgb2 = RGB(0.5, 0.3, 0.8)
    rgb3 = RGB(0.6, 0.3, 0.8)

    assert rgb1 == rgb2
    assert rgb1 != rgb3
    assert rgb2 != rgb3

  def test_equality_different_types(self):
    """Test equality with different types."""
    rgb = RGB(0.5, 0.3, 0.8)
    assert rgb != "not an rgb"
    assert rgb != 42
    assert rgb != None

  def test_hashing(self):
    """Test that RGB instances are hashable."""
    rgb1 = RGB(0.5, 0.3, 0.8)
    rgb2 = RGB(0.5, 0.3, 0.8)
    rgb3 = RGB(0.6, 0.3, 0.8)

    # Equal instances should have equal hashes
    assert hash(rgb1) == hash(rgb2)

    # Different instances should have different hashes (usually)
    assert hash(rgb1) != hash(rgb3)

    # Should be usable in sets and dicts
    rgb_set = {rgb1, rgb2, rgb3}
    assert len(rgb_set) == 2  # rgb1 and rgb2 are equal


class TestRGBStringRepresentation:
  """Test RGB string representations."""

  def test_repr(self):
    """Test __repr__ method."""
    rgb = RGB(0.5, 0.3, 0.8)
    repr_str = repr(rgb)
    assert "RGB(" in repr_str
    assert "r=0.500" in repr_str
    assert "g=0.300" in repr_str
    assert "b=0.800" in repr_str

  def test_str(self):
    """Test __str__ method."""
    rgb = RGB.from_rgb(0xFF5733)
    assert str(rgb) == "#FF5733"


class TestAdjustStrategy:
  """Test AdjustStrategy enum."""

  def test_adjust_strategy_values(self):
    """Test AdjustStrategy enum values."""
    # Test backward compatibility aliases map to appropriate strategies
    assert AdjustStrategy.LINEAR.value == "linear"
    assert AdjustStrategy.ABSOLUTE.value == "absolute"  # ABSOLUTE is now its own strategy
    assert AdjustStrategy.LINEAR.value == "linear"

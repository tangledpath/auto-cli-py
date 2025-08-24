"""Tests for AnsiString ANSI-aware alignment functionality."""

from auto_cli.ansi_string import AnsiString, strip_ansi_codes


class TestStripAnsiCodes:
  """Test ANSI escape code removal functionality."""

  def test_strip_basic_ansi_codes(self):
    """Test removing basic ANSI color codes."""
    # Red text with reset
    colored_text = "\x1b[31mRed\x1b[0m"
    result = strip_ansi_codes(colored_text)
    assert result == "Red"

  def test_strip_complex_ansi_codes(self):
    """Test removing complex ANSI sequences."""
    # Bold red background with blue foreground
    colored_text = "\x1b[1;41;34mComplex\x1b[0m"
    result = strip_ansi_codes(colored_text)
    assert result == "Complex"

  def test_strip_256_color_codes(self):
    """Test removing 256-color ANSI sequences."""
    # 256-color foreground and background
    colored_text = "\x1b[38;5;196mText\x1b[48;5;21m\x1b[0m"
    result = strip_ansi_codes(colored_text)
    assert result == "Text"

  def test_strip_rgb_color_codes(self):
    """Test removing RGB ANSI sequences."""
    # RGB color codes
    colored_text = "\x1b[38;2;255;0;0mRGB\x1b[0m"
    result = strip_ansi_codes(colored_text)
    assert result == "RGB"

  def test_strip_empty_string(self):
    """Test stripping ANSI codes from empty string."""
    assert strip_ansi_codes("") == ""

  def test_strip_none_input(self):
    """Test stripping ANSI codes from None."""
    assert strip_ansi_codes(None) == ""

  def test_strip_no_ansi_codes(self):
    """Test text without ANSI codes remains unchanged."""
    plain_text = "Plain text"
    assert strip_ansi_codes(plain_text) == plain_text

  def test_strip_mixed_content(self):
    """Test text with mixed ANSI codes and plain text."""
    mixed_text = "Start \x1b[31mred\x1b[0m middle \x1b[32mgreen\x1b[0m end"
    result = strip_ansi_codes(mixed_text)
    assert result == "Start red middle green end"


class TestAnsiStringBasic:
  """Test basic AnsiString functionality."""

  def test_init_with_string(self):
    """Test initialization with regular string."""
    ansi_str = AnsiString("Hello")
    assert ansi_str.text == "Hello"
    assert ansi_str.visible_text == "Hello"

  def test_init_with_ansi_string(self):
    """Test initialization with ANSI-coded string."""
    colored_text = "\x1b[31mRed\x1b[0m"
    ansi_str = AnsiString(colored_text)
    assert ansi_str.text == colored_text
    assert ansi_str.visible_text == "Red"

  def test_init_with_none(self):
    """Test initialization with None."""
    ansi_str = AnsiString(None)
    assert ansi_str.text == ""
    assert ansi_str.visible_text == ""

  def test_str_method(self):
    """Test __str__ returns original text with ANSI codes."""
    colored_text = "\x1b[31mRed\x1b[0m"
    ansi_str = AnsiString(colored_text)
    assert str(ansi_str) == colored_text

  def test_repr_method(self):
    """Test __repr__ provides debug representation."""
    ansi_str = AnsiString("test")
    assert repr(ansi_str) == "AnsiString('test')"

  def test_len_method(self):
    """Test __len__ returns visible character count."""
    colored_text = "\x1b[31mRed\x1b[0m"  # 3 visible chars
    ansi_str = AnsiString(colored_text)
    assert len(ansi_str) == 3

  def test_visible_length_property(self):
    """Test visible_length property."""
    colored_text = "\x1b[31mHello\x1b[0m"  # 5 visible chars
    ansi_str = AnsiString(colored_text)
    assert ansi_str.visible_length == 5


class TestAnsiStringAlignment:
  """Test AnsiString format alignment functionality."""

  def test_left_alignment(self):
    """Test left alignment with < specifier."""
    colored_text = "\x1b[31mRed\x1b[0m"  # 3 visible chars
    ansi_str = AnsiString(colored_text)
    result = f"{ansi_str:<10}"
    expected = colored_text + "       "  # 7 spaces to reach width 10
    assert result == expected

  def test_right_alignment(self):
    """Test right alignment with > specifier."""
    colored_text = "\x1b[31mRed\x1b[0m"  # 3 visible chars
    ansi_str = AnsiString(colored_text)
    result = f"{ansi_str:>10}"
    expected = "       " + colored_text  # 7 spaces before text
    assert result == expected

  def test_center_alignment(self):
    """Test center alignment with ^ specifier."""
    colored_text = "\x1b[31mRed\x1b[0m"  # 3 visible chars
    ansi_str = AnsiString(colored_text)
    result = f"{ansi_str:^10}"
    expected = "   " + colored_text + "    "  # 3 + 4 spaces around text
    assert result == expected

  def test_center_alignment_odd_padding(self):
    """Test center alignment with odd padding distribution."""
    colored_text = "\x1b[31mTest\x1b[0m"  # 4 visible chars
    ansi_str = AnsiString(colored_text)
    result = f"{ansi_str:^9}"
    expected = "  " + colored_text + "   "  # 2 + 3 spaces (left gets less)
    assert result == expected

  def test_sign_aware_alignment(self):
    """Test = alignment (treated as right alignment for text)."""
    colored_text = "\x1b[31mText\x1b[0m"  # 4 visible chars
    ansi_str = AnsiString(colored_text)
    result = f"{ansi_str:=10}"
    expected = "      " + colored_text  # 6 spaces before text
    assert result == expected


class TestAnsiStringFillCharacters:
  """Test AnsiString with custom fill characters."""

  def test_custom_fill_left_align(self):
    """Test left alignment with custom fill character."""
    colored_text = "\x1b[31mRed\x1b[0m"
    ansi_str = AnsiString(colored_text)
    result = f"{ansi_str:*<8}"
    expected = colored_text + "*****"  # Fill with asterisks
    assert result == expected

  def test_custom_fill_right_align(self):
    """Test right alignment with custom fill character."""
    colored_text = "\x1b[31mRed\x1b[0m"
    ansi_str = AnsiString(colored_text)
    result = f"{ansi_str:->8}"
    expected = "-----" + colored_text  # Fill with dashes
    assert result == expected

  def test_custom_fill_center_align(self):
    """Test center alignment with custom fill character."""
    colored_text = "\x1b[31mRed\x1b[0m"
    ansi_str = AnsiString(colored_text)
    result = f"{ansi_str:.^9}"
    expected = "..." + colored_text + "..."  # Fill with dots
    assert result == expected


class TestAnsiStringEdgeCases:
  """Test AnsiString edge cases and error handling."""

  def test_no_format_spec(self):
    """Test formatting with empty format spec."""
    colored_text = "\x1b[31mRed\x1b[0m"
    ansi_str = AnsiString(colored_text)
    result = f"{ansi_str}"
    assert result == colored_text

  def test_width_smaller_than_text(self):
    """Test when requested width is smaller than text length."""
    colored_text = "\x1b[31mLongText\x1b[0m"  # 8 visible chars
    ansi_str = AnsiString(colored_text)
    result = f"{ansi_str:<5}"  # Width 5, but text is 8 chars
    assert result == colored_text  # Should return original text

  def test_width_equal_to_text(self):
    """Test when requested width equals text length."""
    colored_text = "\x1b[31mTest\x1b[0m"  # 4 visible chars
    ansi_str = AnsiString(colored_text)
    result = f"{ansi_str:<4}"  # Exact width
    assert result == colored_text

  def test_invalid_format_spec(self):
    """Test handling of invalid format specifications."""
    colored_text = "\x1b[31mTest\x1b[0m"
    ansi_str = AnsiString(colored_text)

    # Invalid width (non-numeric)
    result = f"{ansi_str:<abc}"
    assert result == colored_text  # Should return original text

    # Invalid alignment character
    result = f"{ansi_str:@10}"
    assert result == colored_text  # Should return original text

  def test_zero_width(self):
    """Test formatting with zero width."""
    colored_text = "\x1b[31mTest\x1b[0m"
    ansi_str = AnsiString(colored_text)
    result = f"{ansi_str:<0}"
    assert result == colored_text

  def test_empty_string_formatting(self):
    """Test formatting empty string."""
    ansi_str = AnsiString("")
    result = f"{ansi_str:<10}"
    assert result == "          "  # 10 spaces

  def test_only_ansi_codes(self):
    """Test string containing only ANSI codes."""
    only_ansi = "\x1b[31m\x1b[0m"  # No visible characters
    ansi_str = AnsiString(only_ansi)
    result = f"{ansi_str:<5}"
    assert result == only_ansi + "     "  # 5 spaces added


class TestAnsiStringComparison:
  """Test AnsiString comparison and hashing."""

  def test_equality_with_ansi_string(self):
    """Test equality comparison with another AnsiString."""
    text = "\x1b[31mRed\x1b[0m"
    ansi_str1 = AnsiString(text)
    ansi_str2 = AnsiString(text)
    assert ansi_str1 == ansi_str2

  def test_equality_with_string(self):
    """Test equality comparison with regular string."""
    text = "\x1b[31mRed\x1b[0m"
    ansi_str = AnsiString(text)
    assert ansi_str == text

  def test_inequality_different_text(self):
    """Test inequality with different text."""
    ansi_str1 = AnsiString("\x1b[31mRed\x1b[0m")
    ansi_str2 = AnsiString("\x1b[32mGreen\x1b[0m")
    assert ansi_str1 != ansi_str2

  def test_inequality_with_other_types(self):
    """Test inequality with non-string types."""
    ansi_str = AnsiString("test")
    assert ansi_str != 123
    assert ansi_str != None
    assert ansi_str != []

  def test_hashable(self):
    """Test that AnsiString is hashable."""
    ansi_str = AnsiString("\x1b[31mRed\x1b[0m")
    hash_value = hash(ansi_str)
    assert isinstance(hash_value, int)

    # Same text should produce same hash
    ansi_str2 = AnsiString("\x1b[31mRed\x1b[0m")
    assert hash(ansi_str) == hash(ansi_str2)


class TestAnsiStringMethods:
  """Test additional AnsiString utility methods."""

  def test_startswith_string(self):
    """Test startswith with regular string."""
    colored_text = "\x1b[31mHello World\x1b[0m"
    ansi_str = AnsiString(colored_text)
    assert ansi_str.startswith("Hello")
    assert not ansi_str.startswith("World")

  def test_startswith_ansi_string(self):
    """Test startswith with another AnsiString."""
    colored_text = "\x1b[31mHello World\x1b[0m"
    ansi_str = AnsiString(colored_text)
    prefix_ansi = AnsiString("\x1b[32mHello\x1b[0m")
    assert ansi_str.startswith(prefix_ansi)

  def test_endswith_string(self):
    """Test endswith with regular string."""
    colored_text = "\x1b[31mHello World\x1b[0m"
    ansi_str = AnsiString(colored_text)
    assert ansi_str.endswith("World")
    assert not ansi_str.endswith("Hello")

  def test_endswith_ansi_string(self):
    """Test endswith with another AnsiString."""
    colored_text = "\x1b[31mHello World\x1b[0m"
    ansi_str = AnsiString(colored_text)
    suffix_ansi = AnsiString("\x1b[32mWorld\x1b[0m")
    assert ansi_str.endswith(suffix_ansi)


class TestAnsiStringIntegration:
  """Test AnsiString integration with real ANSI sequences."""

  def test_real_terminal_colors(self):
    """Test with realistic terminal color sequences."""
    # Red bold text
    red_bold = "\x1b[1;31mERROR\x1b[0m"
    ansi_str = AnsiString(red_bold)

    assert ansi_str.visible_text == "ERROR"
    assert len(ansi_str) == 5

    result = f"{ansi_str:>10}"
    expected = "     " + red_bold  # 5 spaces + colored text
    assert result == expected

  def test_multiple_color_changes(self):
    """Test text with multiple color changes."""
    multi_color = "\x1b[31mRed\x1b[32mGreen\x1b[34mBlue\x1b[0m"
    ansi_str = AnsiString(multi_color)

    assert ansi_str.visible_text == "RedGreenBlue"
    assert len(ansi_str) == 12

    result = f"{ansi_str:^20}"
    expected = "    " + multi_color + "    "  # Centered in 20 chars
    assert result == expected

  def test_background_and_foreground(self):
    """Test text with both background and foreground colors."""
    bg_fg = "\x1b[41;37mWhite on Red\x1b[0m"
    ansi_str = AnsiString(bg_fg)

    assert ansi_str.visible_text == "White on Red"
    assert len(ansi_str) == 12

    result = f"{ansi_str:*<20}"
    expected = bg_fg + "********"  # Padded with asterisks
    assert result == expected

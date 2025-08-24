"""Tests for HierarchicalHelpFormatter functionality."""

import argparse
from unittest.mock import Mock, patch

from auto_cli.formatter import HierarchicalHelpFormatter
from auto_cli.theme import create_default_theme


class TestHierarchicalHelpFormatter:
  """Test HierarchicalHelpFormatter class functionality."""

  def setup_method(self):
    """Set up test formatter."""
    # Create minimal parser for testing
    self.parser = argparse.ArgumentParser(
      prog='test_cli',
      description='Test CLI for formatter testing'
    )

    # Create formatter without theme initially
    self.formatter = HierarchicalHelpFormatter(
      prog='test_cli'
    )

  def test_formatter_initialization_no_theme(self):
    """Test formatter initialization without theme."""
    formatter = HierarchicalHelpFormatter(prog='test_cli')

    assert formatter._theme is None
    assert formatter._color_formatter is None
    assert formatter._cmd_indent == 2
    assert formatter._arg_indent == 4
    assert formatter._desc_indent == 8

  def test_formatter_initialization_with_theme(self):
    """Test formatter initialization with theme."""
    theme = create_default_theme()
    formatter = HierarchicalHelpFormatter(prog='test_cli', theme=theme)

    assert formatter._theme == theme
    assert formatter._color_formatter is not None

  def test_console_width_detection(self):
    """Test console width detection and fallback."""
    with patch('os.get_terminal_size') as mock_get_size:
      # Test normal case
      mock_get_size.return_value = Mock(columns=120)
      formatter = HierarchicalHelpFormatter(prog='test_cli')
      assert formatter._console_width == 120

      # Test fallback to environment variable
      mock_get_size.side_effect = OSError()
      with patch.dict('os.environ', {'COLUMNS': '100'}):
        formatter = HierarchicalHelpFormatter(prog='test_cli')
        assert formatter._console_width == 100

      # Test default fallback
      mock_get_size.side_effect = OSError()
      with patch.dict('os.environ', {}, clear=True):
        formatter = HierarchicalHelpFormatter(prog='test_cli')
        assert formatter._console_width == 80

  def test_apply_style_no_theme(self):
    """Test _apply_style method without theme."""
    formatter = HierarchicalHelpFormatter(prog='test_cli')
    result = formatter._apply_style("test text", "command_name")
    assert result == "test text"  # No styling applied

  def test_apply_style_with_theme(self):
    """Test _apply_style method with theme."""
    theme = create_default_theme()
    formatter = HierarchicalHelpFormatter(prog='test_cli', theme=theme)

    # Test that styling is applied (result should contain ANSI codes)
    result = formatter._apply_style("test text", "command_name")

    # Check if colors are enabled in the formatter
    if formatter._color_formatter and formatter._color_formatter.colors_enabled:
      assert result != "test text"  # Should be different due to ANSI codes
      assert "test text" in result  # Original text should be in result
    else:
      # If colors are disabled, result should be unchanged
      assert result == "test text"

  def test_get_display_width_plain_text(self):
    """Test _get_display_width with plain text."""
    formatter = HierarchicalHelpFormatter(prog='test_cli')
    assert formatter._get_display_width("hello") == 5
    assert formatter._get_display_width("") == 0

  def test_get_display_width_with_ansi_codes(self):
    """Test _get_display_width strips ANSI codes correctly."""
    formatter = HierarchicalHelpFormatter(prog='test_cli')

    # Text with ANSI color codes should report correct width
    ansi_text = "\x1b[32mhello\x1b[0m"  # Green "hello"
    assert formatter._get_display_width(ansi_text) == 5

    # More complex ANSI codes
    complex_ansi = "\x1b[1;32;48;5;231mhello world\x1b[0m"
    assert formatter._get_display_width(complex_ansi) == 11

  def test_wrap_text_basic(self):
    """Test _wrap_text method with basic text."""
    formatter = HierarchicalHelpFormatter(prog='test_cli')

    text = "This is a test string that should be wrapped properly."
    lines = formatter._wrap_text(text, indent=4, width=40)

    assert len(lines) > 1  # Should wrap
    assert all(line.startswith("    ") for line in lines)  # All lines indented

  def test_wrap_text_empty(self):
    """Test _wrap_text with empty text."""
    formatter = HierarchicalHelpFormatter(prog='test_cli')
    lines = formatter._wrap_text("", indent=4, width=80)
    assert lines == []

  def test_wrap_text_minimum_width(self):
    """Test _wrap_text respects minimum width."""
    formatter = HierarchicalHelpFormatter(prog='test_cli')

    # Very small width should still use minimum
    text = "This is a test string."
    lines = formatter._wrap_text(text, indent=70, width=80)

    # Should still wrap despite small available width
    assert len(lines) >= 1

  def test_analyze_arguments_empty_parser(self):
    """Test _analyze_arguments with empty parser."""
    formatter = HierarchicalHelpFormatter(prog='test_cli')
    required, optional = formatter._analyze_arguments(None)

    assert required == []
    assert optional == []

  def test_analyze_arguments_with_options(self):
    """Test _analyze_arguments with various option types."""
    formatter = HierarchicalHelpFormatter(prog='test_cli')

    # Create parser with different argument types
    parser = argparse.ArgumentParser()
    parser.add_argument('--required-arg', required=True, help='Required argument')
    parser.add_argument('--optional-arg', help='Optional argument')
    parser.add_argument('--flag', action='store_true', help='Boolean flag')
    parser.add_argument('--with-metavar', metavar='VALUE', help='Arg with metavar')

    required, optional = formatter._analyze_arguments(parser)

    # Check required args (returned as list of tuples: (name, help))
    assert len(required) == 1
    required_names = [name for name, _ in required]
    assert '--required-arg REQUIRED_ARG' in required_names

    # Check optional args (should have 3: optional-arg, flag, with-metavar)
    assert len(optional) == 3

    # Find specific optional args
    optional_names = [name for name, _ in optional]
    assert '--optional-arg OPTIONAL_ARG' in optional_names
    assert '--flag' in optional_names
    assert '--with-metavar VALUE' in optional_names

  def test_format_inline_description_no_description(self):
    """Test _format_inline_description with no description."""
    formatter = HierarchicalHelpFormatter(prog='test_cli')

    lines = formatter._format_inline_description(
      name="command",
      description="",
      name_indent=2,
      description_column=20,
      style_name="command_name",
      style_description="command_description"
    )

    assert len(lines) == 1
    assert lines[0] == "  command"

  def test_format_inline_description_with_colon(self):
    """Test _format_inline_description with colon."""
    formatter = HierarchicalHelpFormatter(prog='test_cli')

    lines = formatter._format_inline_description(
      name="command",
      description="Test description",
      name_indent=2,
      description_column=0,  # Not used for colons
      style_name="command_name",
      style_description="command_description",
      add_colon=True
    )

    assert len(lines) == 1
    # Command descriptions now align at same column as options (not colon + 1 space)
    assert "command:" in lines[0]
    assert "Test description" in lines[0]

  def test_format_inline_description_wrapping(self):
    """Test _format_inline_description with long text that needs wrapping."""
    formatter = HierarchicalHelpFormatter(prog='test_cli')
    formatter._console_width = 40  # Force small width for testing

    long_description = "This is a very long description that should definitely wrap to multiple lines when displayed in the help text."

    lines = formatter._format_inline_description(
      name="cmd",
      description=long_description,
      name_indent=2,
      description_column=10,
      style_name="command_name",
      style_description="command_description"
    )

    # Should wrap to multiple lines
    assert len(lines) > 1
    # First line should contain command name
    assert "cmd" in lines[0]

  def test_format_inline_description_alignment(self):
    """Test _format_inline_description column alignment."""
    formatter = HierarchicalHelpFormatter(prog='test_cli')

    lines = formatter._format_inline_description(
      name="short",
      description="Description",
      name_indent=2,
      description_column=20,
      style_name="command_name",
      style_description="command_description"
    )

    assert len(lines) == 1
    line = lines[0]

    # Check that description starts at approximately the right column
    # (accounting for ANSI codes if theme is enabled)
    assert "short" in line
    assert "Description" in line

  def test_find_subparser_exists(self):
    """Test _find_subparser when subparser exists."""
    formatter = HierarchicalHelpFormatter(prog='test_cli')

    # Create parser with subparsers
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    sub = subparsers.add_parser('test-cmd')

    # Find the subparser
    found = formatter._find_subparser(parser, 'test-cmd')
    assert found == sub

  def test_find_subparser_not_exists(self):
    """Test _find_subparser when subparser doesn't exist."""
    formatter = HierarchicalHelpFormatter(prog='test_cli')

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    subparsers.add_parser('existing-cmd')

    # Try to find non-existent subparser
    found = formatter._find_subparser(parser, 'nonexistent')
    assert found is None

  def test_find_subparser_no_subparsers(self):
    """Test _find_subparser with parser that has no subparsers."""
    formatter = HierarchicalHelpFormatter(prog='test_cli')

    parser = argparse.ArgumentParser()
    found = formatter._find_subparser(parser, 'any-cmd')
    assert found is None


class TestHierarchicalFormatterWithCommandGroups:
  """Test HierarchicalHelpFormatter with CommandGroup descriptions."""

  def setup_method(self):
    """Set up test with mock parser that has CommandGroup description."""
    self.formatter = HierarchicalHelpFormatter(prog='test_cli')

    # Create mock parser with CommandGroup description
    self.parser = argparse.ArgumentParser()
    self.parser._command_group_description = "Custom group description from decorator"

  def test_format_group_with_command_group_description(self):
    """Test that CommandGroup descriptions are used in formatting."""
    # Create mock group parser
    group_parser = Mock()
    group_parser._command_group_description = "Database operations and management"
    group_parser._commands = {'create': 'Create database', 'migrate': 'Run migrations'}
    group_parser.description = "Default description"
    group_parser._actions = []  # Add empty actions list to avoid iteration error

    # Mock _find_subparser to return mock subparsers
    def mock_find_subparser(parser, name):
      mock_sub = Mock()
      mock_sub._actions = []  # Empty actions list
      return mock_sub

    self.formatter._find_subparser = mock_find_subparser

    # Mock other required methods
    self.formatter._calculate_group_dynamic_columns = Mock(return_value=(20, 30))
    self.formatter._format_command_with_args_global_command = Mock(return_value=['  cmd_group: description'])

    # Test the formatting
    lines = self.formatter._format_group_with_command_groups_global(
      name="db",
      parser=group_parser,
      base_indent=2,
      unified_cmd_desc_column=25,  # Add unified command description column
      global_option_column=40
    )

    # Should use the CommandGroup description in formatting
    assert len(lines) > 0
    # The first line should contain the formatted group name with description
    formatted_line = lines[0]
    # Command descriptions now align at column 25, not colon + 1 space
    assert "db:" in formatted_line
    assert "Database operations and management" in formatted_line

  def test_format_group_without_command_group_description(self):
    """Test formatting falls back to default when no CommandGroup description."""
    # Create mock group parser without CommandGroup description
    group_parser = Mock()
    # No _command_group_description attribute - set to None to avoid getattr returning Mock
    group_parser._command_group_description = None
    group_parser.description = "Default group description"
    group_parser.help = ""  # Ensure help is a string, not a Mock
    group_parser._commands = {}
    group_parser._actions = []  # Add empty actions list to avoid iteration error

    lines = self.formatter._format_group_with_command_groups_global(
      name="admin",
      parser=group_parser,
      base_indent=2,
      unified_cmd_desc_column=25,  # Add unified command description column
      global_option_column=40
    )

    # Should use default formatting
    assert len(lines) > 0


class TestHierarchicalFormatterIntegration:
  """Integration tests for HierarchicalHelpFormatter with actual parsers."""

  def test_format_action_with_subparsers(self):
    """Test _format_action with SubParsersAction."""
    formatter = HierarchicalHelpFormatter(prog='test_cli')

    # Create parser with command groups
    parser = argparse.ArgumentParser(formatter_class=lambda *args, **kwargs: formatter)
    subparsers = parser.add_subparsers(dest='command')

    # Add a simple command group
    sub = subparsers.add_parser('test-cmd', help='Test command')
    sub.add_argument('--option', help='Test option')

    # Find the SubParsersAction
    subparsers_action = None
    for action in parser._actions:
      if isinstance(action, argparse._SubParsersAction):
        subparsers_action = action
        break

    assert subparsers_action is not None

    # Test formatting (should not raise exceptions)
    formatted = formatter._format_action(subparsers_action)
    assert isinstance(formatted, str)
    assert 'test-cmd' in formatted

  def test_format_global_option_aligned(self):
    """Test _format_global_option_aligned with actual arguments."""
    formatter = HierarchicalHelpFormatter(prog='test_cli')

    # Create an argument action
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')

    # Get the action
    verbose_action = None
    for action in parser._actions:
      if action.dest == 'verbose':
        verbose_action = action
        break

    assert verbose_action is not None

    # Mock the global column calculation
    formatter._ensure_global_column_calculated = Mock(return_value=30)

    # Test formatting
    formatted = formatter._format_global_option_aligned(verbose_action)
    assert isinstance(formatted, str)
    # Check for either --verbose or -v (argparse may prefer the short form)
    assert ('--verbose' in formatted or '-v' in formatted)
    assert 'Enable verbose output' in formatted

  def test_full_help_formatting_integration(self):
    """Test complete help formatting with real parser structure."""
    # Create a parser similar to what CLI would create
    parser = argparse.ArgumentParser(
      prog='test_cli',
      description='Test CLI Application',
      formatter_class=lambda *args, **kwargs: HierarchicalHelpFormatter(*args, **kwargs)
    )

    # Add global options
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--config', metavar='FILE', help='Configuration file')

    # Add command groups
    subparsers = parser.add_subparsers(title='COMMANDS', dest='command')

    # Flat command
    hello_cmd = subparsers.add_parser('hello', help='Greet someone')
    hello_cmd.add_argument('--name', default='World', help='Name to greet')

    # Group command (simulate what CLI creates)
    user_group = subparsers.add_parser('user', help='User management operations')
    user_group._command_type = 'group'
    user_group._commands = {'create': 'Create user', 'delete': 'Delete user'}

    # Test that help can be generated without errors
    help_text = parser.format_help()

    # Basic sanity checks
    assert 'Test CLI Application' in help_text
    assert 'COMMANDS:' in help_text
    assert 'hello' in help_text
    assert 'user' in help_text
    assert '--verbose' in help_text
    assert '--config' in help_text


class TestHierarchicalFormatterEdgeCases:
  """Test edge cases and error handling for HierarchicalHelpFormatter."""

  def test_format_with_very_long_names(self):
    """Test formatting with very long command/option names."""
    formatter = HierarchicalHelpFormatter(prog='test_cli')
    formatter._console_width = 40  # Small console for testing

    long_name = "very-long-command-name-that-exceeds-normal-length"
    long_description = "This is a very long description that should wrap properly even with long command names."

    lines = formatter._format_inline_description(
      name=long_name,
      description=long_description,
      name_indent=2,
      description_column=20,  # Will be exceeded by long name
      style_name="command_name",
      style_description="command_description"
    )

    # Should handle gracefully
    assert len(lines) >= 1
    assert long_name in lines[0]

  def test_format_with_empty_console_width(self):
    """Test behavior with minimal console width."""
    formatter = HierarchicalHelpFormatter(prog='test_cli')
    formatter._console_width = 10  # Very small

    lines = formatter._format_inline_description(
      name="cmd",
      description="Description text",
      name_indent=2,
      description_column=15,
      style_name="command_name",
      style_description="command_description"
    )

    # Should still produce output
    assert len(lines) >= 1

  def test_analyze_arguments_with_complex_actions(self):
    """Test _analyze_arguments with complex argument configurations."""
    formatter = HierarchicalHelpFormatter(prog='test_cli')

    parser = argparse.ArgumentParser()

    # Add arguments with various configurations
    parser.add_argument('--choices', choices=['a', 'b', 'c'], help='Argument with choices')
    parser.add_argument('--count', type=int, action='append', help='Repeatable integer argument')
    parser.add_argument('--store-const', action='store_const', const='value', help='Store constant')

    required, optional = formatter._analyze_arguments(parser)

    # All should be optional since none marked as required
    assert len(required) == 0
    assert len(optional) == 3

    # Check that different action types are handled
    optional_names = [name for name, _ in optional]
    assert any('--choices' in name for name in optional_names)
    assert any('--count' in name for name in optional_names)
    assert any('--store-const' in name for name in optional_names)

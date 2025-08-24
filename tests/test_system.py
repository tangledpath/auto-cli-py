"""Tests for System class and inner classes."""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from auto_cli import CLI
from auto_cli.system import System


class TestSystem:
  """Test the System class initialization."""

  def test_system_initialization(self):
    """Test System class can be initialized with default config dir."""
    system = System()
    assert system.config_dir == Path.home() / '.auto-cli'

  def test_system_initialization_custom_config(self):
    """Test System class can be initialized with custom config dir."""
    custom_dir = Path("/tmp/test-config")
    system = System(config_dir=custom_dir)
    assert system.config_dir == custom_dir


class TestSystemTuneTheme:
  """Test the System.TuneTheme inner class."""

  def test_tune_theme_initialization_universal(self):
    """Test TuneTheme initializes with universal theme by default."""
    tuner = System().TuneTheme()
    assert tuner.use_colorful_theme is False
    assert tuner.adjust_percent == 0.0
    assert tuner.ADJUSTMENT_INCREMENT == 0.05

  def test_tune_theme_initialization_colorful(self):
    """Test TuneTheme initializes with colorful theme when specified."""
    tuner = System().TuneTheme(initial_theme="colorful")
    assert tuner.use_colorful_theme is True

  def test_increase_adjustment(self):
    """Test adjustment increase functionality."""
    tuner = System().TuneTheme()
    initial_adjustment = tuner.adjust_percent
    tuner.increase_adjustment()
    assert tuner.adjust_percent == initial_adjustment + tuner.ADJUSTMENT_INCREMENT

  def test_decrease_adjustment(self):
    """Test adjustment decrease functionality."""
    tuner = System().TuneTheme()
    tuner.adjust_percent = 0.10  # Set initial value
    tuner.decrease_adjustment()
    assert tuner.adjust_percent == 0.05

  def test_decrease_adjustment_minimum_bound(self):
    """Test adjustment decrease respects minimum bound."""
    tuner = System().TuneTheme()
    tuner.adjust_percent = -5.0  # Set at minimum
    tuner.decrease_adjustment()
    assert tuner.adjust_percent == -5.0  # Should not go lower

  def test_increase_adjustment_maximum_bound(self):
    """Test adjustment increase respects maximum bound."""
    tuner = System().TuneTheme()
    tuner.adjust_percent = 5.0  # Set at maximum
    tuner.increase_adjustment()
    assert tuner.adjust_percent == 5.0  # Should not go higher

  def test_toggle_theme(self):
    """Test theme toggling functionality."""
    tuner = System().TuneTheme()
    assert tuner.use_colorful_theme is False
    tuner.toggle_theme()
    assert tuner.use_colorful_theme is True
    tuner.toggle_theme()
    assert tuner.use_colorful_theme is False

  def test_select_strategy_with_valid_string(self):
    """Test strategy selection with valid string."""
    tuner = System().TuneTheme()
    tuner.select_strategy("COLOR_HSL")
    # Should set strategy without error
    from auto_cli.theme import AdjustStrategy
    assert tuner.adjust_strategy == AdjustStrategy.COLOR_HSL

  def test_select_strategy_with_invalid_string(self):
    """Test strategy selection with invalid string."""
    tuner = System().TuneTheme()
    original_strategy = tuner.adjust_strategy
    tuner.select_strategy("INVALID_STRATEGY")
    # Should not change strategy
    assert tuner.adjust_strategy == original_strategy

  def test_get_current_theme(self):
    """Test getting current theme with adjustments."""
    tuner = System().TuneTheme()
    theme = tuner.get_current_theme()
    assert theme is not None
    # Should return a theme object
    assert hasattr(theme, 'title')
    assert hasattr(theme, 'command_name')

  def test_individual_color_overrides(self):
    """Test individual color override functionality."""
    tuner = System().TuneTheme()
    assert len(tuner.individual_color_overrides) == 0

    # Add a color override
    from auto_cli.theme import RGB
    test_color = RGB.from_rgb(0xFF0000)  # Red
    tuner.individual_color_overrides['title'] = test_color
    tuner.modified_components.add('title')

    assert len(tuner.individual_color_overrides) == 1
    assert 'title' in tuner.modified_components

    # Get theme with overrides
    theme = tuner.get_current_theme()
    assert theme.title.fg == test_color

  def test_reset_component_color(self):
    """Test resetting individual component colors."""
    tuner = System().TuneTheme()
    from auto_cli.theme import RGB
    test_color = RGB.from_rgb(0xFF0000)

    # Add override then reset
    tuner.individual_color_overrides['title'] = test_color
    tuner.modified_components.add('title')
    tuner._reset_component_color('title')

    assert 'title' not in tuner.individual_color_overrides
    assert 'title' not in tuner.modified_components

  def test_reset_all_individual_colors(self):
    """Test resetting all individual colors."""
    tuner = System().TuneTheme()
    from auto_cli.theme import RGB

    # Add multiple overrides
    tuner.individual_color_overrides['title'] = RGB.from_rgb(0xFF0000)
    tuner.individual_color_overrides['command_name'] = RGB.from_rgb(0x00FF00)
    tuner.modified_components.update(['title', 'command_name'])

    tuner._reset_all_individual_colors()

    assert len(tuner.individual_color_overrides) == 0
    assert len(tuner.modified_components) == 0


class TestSystemCompletion:
  """Test the System.Completion inner class."""

  def test_completion_initialization(self):
    """Test Completion class initializes correctly."""
    completion = System().Completion()
    assert completion.shell == "bash"
    assert completion._cli_instance is None
    assert completion._completion_handler is None

  def test_completion_initialization_with_cli(self):
    """Test Completion class initializes with CLI instance."""
    mock_cli = MagicMock()
    completion = System.Completion(cli_instance=mock_cli)
    assert completion._cli_instance == mock_cli

  def test_is_completion_request_false(self):
    """Test completion request detection returns False normally."""
    completion = System().Completion()
    # Patch sys.argv to not include completion flags
    with patch.object(sys, 'argv', ['script.py']):
      with patch('os.environ.get', return_value=None):
        assert completion.is_completion_request() is False

  def test_is_completion_request_true_argv(self):
    """Test completion request detection returns True with --_complete flag."""
    completion = System().Completion()
    with patch.object(sys, 'argv', ['script.py', '--_complete']):
      assert completion.is_completion_request() is True

  def test_is_completion_request_true_env(self):
    """Test completion request detection returns True with env var."""
    completion = System().Completion()
    with patch.object(sys, 'argv', ['script.py']):
      with patch('os.environ.get', return_value='1'):
        assert completion.is_completion_request() is True

  def test_install_completion_disabled(self):
    """Test install completion when completion is disabled."""
    mock_cli = MagicMock()
    mock_cli.enable_completion = False
    completion = System.Completion(cli_instance=mock_cli)

    result = completion.install()
    assert result is False

  def test_show_completion_disabled(self):
    """Test show completion when completion is disabled."""
    mock_cli = MagicMock()
    mock_cli.enable_completion = False
    completion = System.Completion(cli_instance=mock_cli)

    # Should not raise error, just print message
    completion.show("bash")

  def test_install_completion_no_cli_instance(self):
    """Test install completion without CLI instance."""
    completion = System().Completion()
    result = completion.install()
    assert result is False

  @patch('sys.exit')
  def test_handle_completion_no_handler(self, mock_exit):
    """Test handle completion without completion handler."""
    completion = System().Completion()
    # Mock the init_completion to prevent actually initializing
    with patch.object(completion, 'init_completion'):
      completion.handle_completion()
      # Should call exit once with code 1 when no handler is available
      mock_exit.assert_called_once_with(1)


class TestSystemCLIGeneration:
  """Test System class CLI generation."""

  def test_system_cli_generation(self):
    """Test System class generates CLI correctly."""
    cli = CLI(System)
    parser = cli.create_parser()

    # Should have System class as target
    assert cli.target_class == System
    assert cli.target_mode.value == 'class'

  def test_system_cli_has_inner_classes(self):
    """Test System CLI recognizes inner classes."""
    cli = CLI(System)

    # Should discover inner classes
    assert hasattr(cli, 'inner_classes')
    assert 'TuneTheme' in cli.inner_classes
    assert 'Completion' in cli.inner_classes

  def test_system_cli_command_structure(self):
    """Test System CLI creates proper command structure."""
    cli = CLI(System)

    # Should have hierarchical commands  
    assert 'tune-theme' in cli.commands
    assert 'completion' in cli.commands

    # Groups should have hierarchical structure
    tune_theme_group = cli.commands['tune-theme']
    assert tune_theme_group['type'] == 'group'
    assert 'increase-adjustment' in tune_theme_group['commands']
    assert 'decrease-adjustment' in tune_theme_group['commands']

    completion_group = cli.commands['completion']
    assert completion_group['type'] == 'group'
    assert 'install' in completion_group['commands']
    assert 'show' in completion_group['commands']

  def test_system_tune_theme_methods(self):
    """Test System CLI includes TuneTheme methods as hierarchical command groups."""
    cli = CLI(System)

    # Check that TuneTheme methods are included as commands under tune-theme group
    tune_theme_group = cli.commands['tune-theme']
    expected_commands = [
      'increase-adjustment', 'decrease-adjustment',
      'select-strategy', 'toggle-theme',
      'edit-colors', 'show-rgb', 'run-interactive'
    ]

    for command in expected_commands:
      assert command in tune_theme_group['commands']
      assert tune_theme_group['commands'][command]['type'] == 'command'

  def test_system_completion_methods(self):
    """Test System CLI includes Completion methods as hierarchical command groups."""
    cli = CLI(System)

    # Check that Completion methods are included as commands under completion group
    completion_group = cli.commands['completion']
    expected_commands = ['install', 'show']

    for command in expected_commands:
      assert command in completion_group['commands']
      assert completion_group['commands'][command]['type'] == 'command'

  def test_system_cli_execution(self):
    """Test System CLI can execute commands."""
    cli = CLI(System)

    # Test that we can create a parser without errors
    parser = cli.create_parser()
    assert parser is not None

    # Test parsing a valid hierarchical command
    args = parser.parse_args(['tune-theme', 'toggle-theme'])
    assert hasattr(args, '_cli_function')
    assert args._cli_function is not None


class TestSystemIntegration:
  """Integration tests for System class with CLI."""

  def test_system_help_generation(self):
    """Test System CLI generates help correctly."""
    cli = CLI(System, title="System Test CLI")
    parser = cli.create_parser()

    help_text = parser.format_help()

    # Should contain main sections
    assert "System Test CLI" in help_text
    assert "tune-theme" in help_text
    assert "completion" in help_text

  def test_system_command_group_help(self):
    """Test System CLI command group help generation."""
    cli = CLI(System)
    parser = cli.create_parser()

    # Test that parsing to command level works (help would exit)
    with pytest.raises(SystemExit):
      parser.parse_args(['tune-theme', '--help'])

  def test_system_backwards_compatibility(self):
    """Test backwards compatibility with old ThemeTuner usage."""
    from auto_cli.theme.theme_tuner import ThemeTuner, run_theme_tuner

    # Should be able to import and create instances (with warnings)
    with pytest.warns(DeprecationWarning):
      tuner = ThemeTuner()

    assert tuner is not None

    # Should be able to call run_theme_tuner (patch to avoid interactive input)
    with pytest.warns(DeprecationWarning):
      with patch('auto_cli.system.System.TuneTheme.run_interactive'):
        run_theme_tuner("universal")


if __name__ == '__main__':
  pytest.main([__file__])

"""Tests for hierarchical command groups functionality with double underscore delimiter."""

import enum
import sys
from unittest.mock import patch

import pytest

from auto_cli.cli import CLI


class UserRole(enum.Enum):
  """Test role enumeration."""
  USER = "user"
  ADMIN = "admin"


# Test functions for hierarchical commands
def flat_hello(name: str = "World"):
  """Simple flat command.

  :param name: Name to greet
  """
  return f"Hello, {name}!"


def user__create(username: str, email: str, role: UserRole = UserRole.USER):
  """Create a new user.

  :param username: Username for the account
  :param email: Email address
  :param role: User role
  """
  return f"Created user {username} ({email}) with role {role.value}"


def user__list(active_only: bool = False, limit: int = 10):
  """List users with filtering.

  :param active_only: Show only active users
  :param limit: Maximum number of users to show
  """
  return f"Listing users (active_only={active_only}, limit={limit})"


def user__delete(username: str, force: bool = False):
  """Delete a user account.

  :param username: Username to delete
  :param force: Skip confirmation
  """
  return f"Deleted user {username} (force={force})"


def db__migrate(steps: int = 1, direction: str = "up"):
  """Run database migrations.

  :param steps: Number of steps
  :param direction: Migration direction
  """
  return f"Migrating {steps} steps {direction}"


def admin__user__reset_password(username: str, notify: bool = True):
  """Reset user password (admin operation).

  :param username: Username to reset
  :param notify: Send notification
  """
  return f"Admin reset password for {username} (notify={notify})"


def admin__system__backup(compress: bool = True):
  """Create system backup.

  :param compress: Compress backup
  """
  return f"System backup (compress={compress})"


# Create test module
test_module = sys.modules[__name__]


class TestHierarchicalCommandGroups:
  """Test hierarchical command group functionality."""

  def setup_method(self):
    """Set up test CLI instance."""
    self.cli = CLI(test_module, "Test CLI with Hierarchical Commands")

  def test_function_discovery_and_grouping(self):
    """Test that functions are correctly discovered as flat commands (no grouping)."""
    commands = self.cli.commands

    # Check flat command
    assert "flat-hello" in commands
    assert commands["flat-hello"]["type"] == "command"
    assert commands["flat-hello"]["function"] == flat_hello

    # Check user commands (now flat with double-dash)
    assert "user--create" in commands
    assert commands["user--create"]["type"] == "command"
    assert commands["user--create"]["function"] == user__create

    assert "user--list" in commands
    assert commands["user--list"]["type"] == "command"
    assert commands["user--list"]["function"] == user__list

    assert "user--delete" in commands
    assert commands["user--delete"]["type"] == "command"
    assert commands["user--delete"]["function"] == user__delete

    # Check db commands (now flat with double-dash)
    assert "db--migrate" in commands
    assert commands["db--migrate"]["type"] == "command"
    assert commands["db--migrate"]["function"] == db__migrate

    # Check nested admin commands (now flat with double-dash)
    assert "admin--user--reset-password" in commands
    assert commands["admin--user--reset-password"]["type"] == "command"
    assert commands["admin--user--reset-password"]["function"] == admin__user__reset_password

    assert "admin--system--backup" in commands
    assert commands["admin--system--backup"]["type"] == "command"
    assert commands["admin--system--backup"]["function"] == admin__system__backup

  def test_parser_creation_flat_commands(self):
    """Test parser creation with flat commands only."""
    parser = self.cli.create_parser()

    # Test that parser has subparsers
    subparsers_action = None
    for action in parser._actions:
      if hasattr(action, 'choices') and action.choices:
        subparsers_action = action
        break

    assert subparsers_action is not None
    choices = list(subparsers_action.choices.keys())

    # Should have flat commands only
    assert "flat-hello" in choices
    assert "user--create" in choices
    assert "user--list" in choices
    assert "user--delete" in choices
    assert "db--migrate" in choices
    assert "admin--user--reset-password" in choices
    assert "admin--system--backup" in choices

  def test_flat_command_execution(self):
    """Test execution of flat commands."""
    result = self.cli.run(["flat-hello", "--name", "Alice"])
    assert result == "Hello, Alice!"

  def test_flat_command_execution_with_args(self):
    """Test execution of flat commands with arguments."""
    # Test user create (now flat command)
    result = self.cli.run([
      "user--create",
      "--username", "alice",
      "--email", "alice@test.com",
      "--role", "ADMIN"
    ])
    assert result == "Created user alice (alice@test.com) with role admin"

    # Test user list (now flat command)
    result = self.cli.run(["user--list", "--active-only", "--limit", "5"])
    assert result == "Listing users (active_only=True, limit=5)"

    # Test db migrate (now flat command)
    result = self.cli.run(["db--migrate", "--steps", "3", "--direction", "down"])
    assert result == "Migrating 3 steps down"

  def test_deeply_nested_flat_command_execution(self):
    """Test execution of deeply nested commands as flat commands."""
    # Test admin user reset-password (notify is True by default)
    result = self.cli.run([
      "admin--user--reset-password",
      "--username", "bob"
    ])
    assert result == "Admin reset password for bob (notify=True)"

    # Test admin system backup (compress is True by default)
    result = self.cli.run([
      "admin--system--backup"
    ])
    assert result == "System backup (compress=True)"

  def test_help_display_main(self):
    """Test main help displays hierarchical structure."""
    with patch('sys.stdout') as mock_stdout:
      with pytest.raises(SystemExit):
        self.cli.run(["--help"])

    # Should have called print_help
    assert mock_stdout.write.called

  def test_help_display_flat_command(self):
    """Test flat command help."""
    # Flat commands don't have group help - they execute directly or show command help
    with patch('sys.stdout') as mock_stdout:
      with pytest.raises(SystemExit):
        self.cli.run(["user--create", "--help"])

    # Should have called help output
    assert mock_stdout.write.called

  def test_help_display_deeply_nested_flat_command(self):
    """Test deeply nested flat command help."""
    # No nested groups - all commands are flat
    with patch('sys.stdout') as mock_stdout:
      with pytest.raises(SystemExit):
        self.cli.run(["admin--system--backup", "--help"])

    # Should have called help output
    assert mock_stdout.write.called

  def test_missing_command_handling(self):
    """Test handling of missing commands."""
    with patch('builtins.print') as mock_print:
      result = self.cli.run([])

    # Should show main help and return 0
    assert result == 0

  def test_invalid_command_handling(self):
    """Test handling of invalid commands."""
    with patch('builtins.print') as mock_print:
      with patch('sys.stderr'):
        with pytest.raises(SystemExit):
          result = self.cli.run(["nonexistent"])

  def test_underscore_to_dash_conversion(self):
    """Test that underscores are converted to dashes in CLI names."""
    commands = self.cli.commands

    # Check that function names with underscores become dashed
    assert "flat-hello" in commands  # flat_hello -> flat-hello

    # Check flat commands with double-dash conversion
    assert "user--create" in commands  # user__create -> user--create
    assert "admin--user--reset-password" in commands  # admin__user__reset_password -> admin--user--reset-password
    assert "admin--system--backup" in commands  # admin__system__backup -> admin--system--backup

  def test_command_original_name_storage(self):
    """Test that original function names are stored correctly for flat commands."""
    commands = self.cli.commands

    # Check original function name storage
    reset_cmd = commands["admin--user--reset-password"]
    assert reset_cmd["original_name"] == "admin__user__reset_password"

    backup_cmd = commands["admin--system--backup"]
    assert backup_cmd["original_name"] == "admin__system__backup"

  def test_mixed_simple_and_complex_flat_commands(self):
    """Test CLI with mix of simple and complex flat commands."""
    # Should be able to execute both simple and complex flat commands
    simple_result = self.cli.run(["flat-hello", "--name", "Test"])
    assert simple_result == "Hello, Test!"

    complex_result = self.cli.run(["user--create", "--username", "test", "--email", "test@test.com"])
    assert "Created user test" in complex_result

  def test_error_handling_with_verbose(self):
    """Test error handling with verbose flag."""

    # Create a CLI with a function that will raise an error
    def error_function():
      """Function that raises an error."""
      raise ValueError("Test error")

    # Add the function to the test module temporarily
    test_module.error_function = error_function

    try:
      error_cli = CLI(test_module, "Error Test CLI")

      with patch('builtins.print') as mock_print:
        with patch('sys.stderr'):
          result = error_cli.run(["--verbose", "error-function"])

      # Should return error code
      assert result == 1

    finally:
      # Clean up
      if hasattr(test_module, 'error_function'):
        delattr(test_module, 'error_function')


class TestHierarchicalEdgeCases:
  """Test edge cases for hierarchical command groups."""

  def test_empty_double_underscore(self):
    """Test handling of functions with empty parts in double underscore."""

    # This would be malformed: user__  or __create
    # The function discovery should handle gracefully
    def malformed__function():
      """Malformed function name."""
      return "test"

    # Should not crash during discovery
    cli = CLI(sys.modules[__name__], "Test CLI")
    # The function shouldn't be included in normal discovery due to naming

  def test_single_vs_double_underscore_distinction(self):
    """Test that both single and double underscores create flat commands."""

    def single_underscore_func():
      """Function with single underscore."""
      return "single"

    def double__underscore__func():
      """Function with double underscore."""
      return "double"

    # Add to module temporarily
    test_module.single_underscore_func = single_underscore_func
    test_module.double__underscore__func = double__underscore__func

    try:
      cli = CLI(test_module, "Test CLI")
      commands = cli.commands

      # Single underscore should be flat command with dash
      assert "single-underscore-func" in commands
      assert commands["single-underscore-func"]["type"] == "command"

      # Double underscore should also create flat command (no groups)
      assert "double--underscore--func" in commands
      assert commands["double--underscore--func"]["type"] == "command"

    finally:
      # Clean up
      delattr(test_module, 'single_underscore_func')
      delattr(test_module, 'double__underscore__func')

  def test_deep_nesting_as_flat_command(self):
    """Test that deep nesting creates flat commands."""

    def level1__level2__level3__level4__deep_command():
      """Very deeply nested command."""
      return "deep"

    # Add to module temporarily
    test_module.level1__level2__level3__level4__deep_command = level1__level2__level3__level4__deep_command

    try:
      cli = CLI(test_module, "Test CLI")
      commands = cli.commands

      # Should create flat command with multiple dashes
      assert "level1--level2--level3--level4--deep-command" in commands
      assert commands["level1--level2--level3--level4--deep-command"]["type"] == "command"

    finally:
      # Clean up
      delattr(test_module, 'level1__level2__level3__level4__deep_command')

#!/usr/bin/env python
"""Comprehensive tests for module-based CLI functionality."""

import enum
import sys
from pathlib import Path
from typing import List, Optional

import pytest

from auto_cli.cli import CLI


# ==================== TEST MODULE FUNCTIONS ====================

class DataFormat(enum.Enum):
  """Test data formats."""
  JSON = "json"
  CSV = "csv"
  YAML = "yaml"


class Priority(enum.Enum):
  """Test priority levels."""
  LOW = "low"
  MEDIUM = "medium"
  HIGH = "high"


def simple_function(name: str, age: int = 25) -> dict:
  """A simple function for testing.

  :param name: Person's name
  :param age: Person's age
  """
  return {"name": name, "age": age}


def process_data(input_file: Path, output_format: DataFormat = DataFormat.JSON,
                 verbose: bool = False) -> dict:
  """Process data file and convert to specified format.

  :param input_file: Path to input data file
  :param output_format: Output format for processed data
  :param verbose: Enable verbose output during processing
  """
  return {
    "input_file": str(input_file),
    "output_format": output_format.value,
    "verbose": verbose
  }


def analyze_logs(log_file: Path, pattern: str, max_lines: int = 1000,
                 case_sensitive: bool = True) -> dict:
  """Analyze log files for specific patterns.

  :param log_file: Path to log file to analyze
  :param pattern: Pattern to search for in logs
  :param max_lines: Maximum number of lines to analyze
  :param case_sensitive: Whether pattern matching is case sensitive
  """
  return {
    "log_file": str(log_file),
    "pattern": pattern,
    "max_lines": max_lines,
    "case_sensitive": case_sensitive
  }


def backup_create(source_dir: Path, destination: str, compress: bool = True) -> dict:
  """Create backup of source directory.

  :param source_dir: Source directory to backup
  :param destination: Destination path for backup
  :param compress: Whether to compress the backup
  """
  return {
    "source_dir": str(source_dir),
    "destination": destination,
    "compress": compress
  }


def backup_restore(backup_file: Path, target_dir: Path,
                   overwrite: bool = False) -> dict:
  """Restore from backup file.

  :param backup_file: Backup file to restore from
  :param target_dir: Target directory for restoration
  :param overwrite: Whether to overwrite existing files
  """
  return {
    "backup_file": str(backup_file),
    "target_dir": str(target_dir),
    "overwrite": overwrite
  }


def set_config_value(key: str, value: str, global_config: bool = False) -> dict:
  """Set configuration value.

  :param key: Configuration key to set
  :param value: Value to set for the key
  :param global_config: Whether to set in global configuration
  """
  return {
    "key": key,
    "value": value,
    "global_config": global_config
  }


def get_config_value(key: str, default_value: str = "none") -> dict:
  """Get configuration value.

  :param key: Configuration key to retrieve
  :param default_value: Default value if key not found
  """
  return {
    "key": key,
    "default_value": default_value
  }


def create_task(title: str, priority: Priority = Priority.MEDIUM,
                due_date: Optional[str] = None, tags: Optional[List[str]] = None) -> dict:
  """Create a new task.

  :param title: Task title
  :param priority: Task priority level
  :param due_date: Due date for task (ISO format)
  :param tags: List of tags for the task
  """
  return {
    "title": title,
    "priority": priority.value,
    "due_date": due_date,
    "tags": tags or []
  }


def list_tasks(status: str = "all", priority_filter: Priority = Priority.MEDIUM,
               show_completed: bool = False) -> dict:
  """List tasks with filtering options.

  :param status: Task status filter
  :param priority_filter: Filter by priority level
  :param show_completed: Whether to show completed tasks
  """
  return {
    "status": status,
    "priority_filter": priority_filter.value,
    "show_completed": show_completed
  }


def export_data(format: DataFormat = DataFormat.JSON, output_file: Optional[Path] = None,
                include_metadata: bool = True) -> dict:
  """Export data to specified format.

  :param format: Export format
  :param output_file: Output file path
  :param include_metadata: Whether to include metadata in export
  """
  return {
    "format": format.value,
    "output_file": str(output_file) if output_file else None,
    "include_metadata": include_metadata
  }


# Helper function that should be ignored (starts with underscore)
def _private_helper(data: str) -> str:
  """Private helper function that should not be exposed in CLI."""
  return f"processed_{data}"


# ==================== MODULE CLI TESTS ====================

class TestModuleCLI:
  """Test module-based CLI functionality."""

  def create_test_cli(self):
    """Create CLI from current module for testing."""
    return CLI(sys.modules[__name__], "Test Module CLI")

  def test_module_function_discovery(self):
    """Test that module functions are discovered correctly."""
    cli = self.create_test_cli()

    # Should have discovered public functions (all flat now)
    expected_functions = {
      'simple_function', 'process_data', 'analyze_logs',
      'backup_create', 'backup_restore',
      'set_config_value', 'get_config_value',
      'create_task', 'list_tasks',
      'export_data'
    }

    discovered_functions = set(cli.functions.keys())

    # Check that all expected functions are discovered
    for func_name in expected_functions:
      assert func_name in discovered_functions, f"Function {func_name} not discovered"

    # Should not discover private functions
    assert '_private_helper' not in discovered_functions

  def test_command_structure_generation(self):
    """Test command structure generation from functions."""
    cli = self.create_test_cli()

    # Should have flat commands
    assert 'simple-function' in cli.commands
    assert cli.commands['simple-function']['type'] == 'command'

    assert 'process-data' in cli.commands
    assert cli.commands['process-data']['type'] == 'command'

    # Should have flat commands only
    assert 'backup-create' in cli.commands
    assert cli.commands['backup-create']['type'] == 'command'

    assert 'set-config-value' in cli.commands
    assert cli.commands['set-config-value']['type'] == 'command'

    assert 'create-task' in cli.commands
    assert cli.commands['create-task']['type'] == 'command'

  def test_flat_command_execution(self):
    """Test execution of flat commands."""
    cli = self.create_test_cli()

    # Test simple function
    test_args = ['simple-function', '--name', 'Alice', '--age', '30']
    result = cli.run(test_args)

    assert result['name'] == 'Alice'
    assert result['age'] == 30

  def test_flat_command_execution(self):
    """Test execution of flat commands."""
    cli = self.create_test_cli()

    # Test backup create (now flat command)
    test_args = ['backup-create', '--source-dir', '/home/user',
                 '--destination', '/backup/user', '--compress']
    result = cli.run(test_args)

    assert result['source_dir'] == '/home/user'
    assert result['destination'] == '/backup/user'
    assert result['compress'] is True

  def test_enum_parameter_handling(self):
    """Test enum parameters in module functions."""
    cli = self.create_test_cli()

    # Test with enum parameter
    test_args = ['process-data', '--input-file', 'data.txt',
                 '--output-format', 'CSV', '--verbose']
    result = cli.run(test_args)

    assert result['input_file'] == 'data.txt'
    assert result['output_format'] == 'csv'
    assert result['verbose'] is True

  def test_optional_parameters(self):
    """Test optional parameters with defaults."""
    cli = self.create_test_cli()

    # Test with all parameters
    test_args = ['analyze-logs', '--log-file', 'app.log', '--pattern', 'ERROR',
                 '--max-lines', '5000', '--case-sensitive']
    result = cli.run(test_args)

    assert result['log_file'] == 'app.log'
    assert result['pattern'] == 'ERROR'
    assert result['max_lines'] == 5000
    assert result['case_sensitive'] is True

    # Test with defaults
    test_args = ['analyze-logs', '--log-file', 'app.log', '--pattern', 'WARNING']
    result = cli.run(test_args)

    assert result['log_file'] == 'app.log'
    assert result['pattern'] == 'WARNING'
    assert result['max_lines'] == 1000  # Default value
    assert result['case_sensitive'] is True  # Default value

  def test_path_type_handling(self):
    """Test Path type annotations."""
    cli = self.create_test_cli()

    test_args = ['backup-restore', '--backup-file', 'backup.tar.gz',
                 '--target-dir', '/restore/path']
    result = cli.run(test_args)

    assert result['backup_file'] == 'backup.tar.gz'
    assert result['target_dir'] == '/restore/path'

  def test_optional_path_handling(self):
    """Test Optional[Path] type annotations."""
    cli = self.create_test_cli()

    # Test with optional path
    test_args = ['export-data', '--format', 'YAML', '--output-file', 'output.yaml']
    result = cli.run(test_args)

    assert result['format'] == 'yaml'
    assert result['output_file'] == 'output.yaml'

    # Test without optional path
    test_args = ['export-data', '--format', 'JSON']
    result = cli.run(test_args)

    assert result['format'] == 'json'
    assert result['output_file'] is None

  def test_list_type_handling(self):
    """Test List type annotations (should be handled gracefully)."""
    cli = self.create_test_cli()

    # Note: List types are complex and may not be fully supported
    # But the CLI should handle them without crashing
    test_args = ['create-task', '--title', 'Test Task', '--priority', 'HIGH']
    result = cli.run(test_args)

    assert result['title'] == 'Test Task'
    assert result['priority'] == 'high'

  def test_help_generation(self):
    """Test help text generation."""
    cli = self.create_test_cli()
    parser = cli.create_parser()

    help_text = parser.format_help()

    # Should show flat commands
    assert 'simple-function' in help_text
    assert 'process-data' in help_text

    # Should show flat commands
    assert 'backup-create' in help_text
    assert 'backup-restore' in help_text
    assert 'set-config-value' in help_text
    assert 'get-config-value' in help_text

  def test_command_help(self):
    """Test help for flat commands."""
    cli = self.create_test_cli()

    # Test that we can parse help for commands without errors
    with pytest.raises(SystemExit):  # argparse exits after showing help
      cli.run(['backup-create', '--help'])


class TestModuleCLIFiltering:
  """Test function filtering in module CLI."""

  def test_custom_function_filter(self):
    """Test custom function filtering."""

    def custom_filter(name: str, obj) -> bool:
      # Only include functions that start with 'process'
      return (name.startswith('process') and
              callable(obj) and
              not name.startswith('_'))

    cli = CLI(sys.modules[__name__], "Filtered CLI",
              function_filter=custom_filter)

    # Should only have process_data function
    assert 'process_data' in cli.functions
    assert 'simple_function' not in cli.functions
    assert 'analyze_logs' not in cli.functions

  def test_default_function_filter(self):
    """Test default function filtering behavior."""
    cli = CLI(sys.modules[__name__], "Test CLI")

    # Should exclude private functions
    assert '_private_helper' not in cli.functions

    # Should exclude imported functions and classes
    assert 'pytest' not in cli.functions
    assert 'Path' not in cli.functions
    assert 'CLI' not in cli.functions

    # Should include module-defined functions
    assert 'simple_function' in cli.functions


class TestModuleCLIErrorHandling:
  """Test error handling for module CLI."""

  def test_missing_required_parameter(self):
    """Test handling of missing required parameters."""
    cli = CLI(sys.modules[__name__], "Test CLI")

    # Should raise SystemExit when required parameter is missing
    with pytest.raises(SystemExit):
      cli.run(['simple-function'])  # Missing --name

  def test_invalid_enum_value(self):
    """Test handling of invalid enum values."""
    cli = CLI(sys.modules[__name__], "Test CLI")

    # Should raise SystemExit for invalid enum value
    with pytest.raises(SystemExit):
      cli.run(['process-data', '--input-file', 'test.txt',
               '--output-format', 'INVALID'])

  def test_invalid_command(self):
    """Test handling of invalid commands."""
    cli = CLI(sys.modules[__name__], "Test CLI")

    # Should raise SystemExit for invalid command
    with pytest.raises(SystemExit):
      cli.run(['nonexistent-command'])

  def test_invalid_command(self):
    """Test handling of invalid commands."""
    cli = CLI(sys.modules[__name__], "Test CLI")

    # Should raise SystemExit for invalid command
    with pytest.raises(SystemExit):
      cli.run(['invalid-command'])


class TestModuleCLITypeConversion:
  """Test type conversion for module CLI."""

  def test_integer_conversion(self):
    """Test integer parameter conversion."""
    cli = CLI(sys.modules[__name__], "Test CLI")

    test_args = ['simple-function', '--name', 'Bob', '--age', '45']
    result = cli.run(test_args)

    assert isinstance(result['age'], int)
    assert result['age'] == 45

  def test_boolean_conversion(self):
    """Test boolean parameter conversion."""
    cli = CLI(sys.modules[__name__], "Test CLI")

    # Test boolean flag set
    test_args = ['process-data', '--input-file', 'test.txt', '--verbose']
    result = cli.run(test_args)

    assert isinstance(result['verbose'], bool)
    assert result['verbose'] is True

    # Test boolean flag not set
    test_args = ['process-data', '--input-file', 'test.txt']
    result = cli.run(test_args)

    assert isinstance(result['verbose'], bool)
    assert result['verbose'] is False

  def test_path_conversion(self):
    """Test Path type conversion."""
    cli = CLI(sys.modules[__name__], "Test CLI")

    test_args = ['process-data', '--input-file', '/path/to/file.txt']
    result = cli.run(test_args)

    # Result should be string representation of Path
    assert result['input_file'] == '/path/to/file.txt'


class TestModuleCLICommandGrouping:
  """Test command grouping in module CLI."""

  def test_flat_command_structure(self):
    """Test that all functions create flat commands in modules."""
    cli = CLI(sys.modules[__name__], "Test CLI")

    # Should create flat commands (no groups)
    assert 'backup-create' in cli.commands
    assert cli.commands['backup-create']['type'] == 'command'

    assert 'backup-restore' in cli.commands
    assert cli.commands['backup-restore']['type'] == 'command'

    assert 'set-config-value' in cli.commands
    assert cli.commands['set-config-value']['type'] == 'command'

    assert 'get-config-value' in cli.commands
    assert cli.commands['get-config-value']['type'] == 'command'

    assert 'create-task' in cli.commands
    assert cli.commands['create-task']['type'] == 'command'

    assert 'list-tasks' in cli.commands
    assert cli.commands['list-tasks']['type'] == 'command'

  def test_all_flat_commands(self):
    """Test that modules only support flat commands."""
    cli = CLI(sys.modules[__name__], "Test CLI")

    # Should have all flat commands only
    assert 'simple-function' in cli.commands
    assert 'process-data' in cli.commands
    assert 'export-data' in cli.commands
    assert 'backup-create' in cli.commands
    assert 'backup-restore' in cli.commands
    assert 'set-config-value' in cli.commands
    assert 'get-config-value' in cli.commands
    assert 'create-task' in cli.commands
    assert 'list-tasks' in cli.commands

    # All commands should be type 'command' in modules (flat structure)
    assert cli.commands['simple-function']['type'] == 'command'
    assert cli.commands['export-data']['type'] == 'command'
    assert cli.commands['backup-create']['type'] == 'command'
    assert cli.commands['set-config-value']['type'] == 'command'


if __name__ == '__main__':
  pytest.main([__file__])

"""Tests for mod_example.py functionality."""
import subprocess
import sys
from pathlib import Path


class TestModuleExample:
  """Test cases for the mod_example.py file."""

  def test_examples_help(self):
    """Test that mod_example.py shows help without errors."""
    examples_path = Path(__file__).parent.parent / "mod_example.py"
    result = subprocess.run(
      [sys.executable, str(examples_path), "--help"],
      capture_output=True,
      text=True,
      timeout=10
    )

    assert result.returncode == 0
    assert "Usage:" in result.stdout or "usage:" in result.stdout

  def test_examples_foo_command(self):
    """Test the foo command in mod_example.py."""
    examples_path = Path(__file__).parent.parent / "mod_example.py"
    result = subprocess.run(
      [sys.executable, str(examples_path), "foo"],
      capture_output=True,
      text=True,
      timeout=10
    )

    assert result.returncode == 0
    assert "FOO!" in result.stdout

  def test_examples_train_command_help(self):
    """Test the train command help in mod_example.py."""
    examples_path = Path(__file__).parent.parent / "mod_example.py"
    result = subprocess.run(
      [sys.executable, str(examples_path), "train", "--help"],
      capture_output=True,
      text=True,
      timeout=10
    )

    assert result.returncode == 0
    assert "data-dir" in result.stdout
    assert "initial-learning-rate" in result.stdout

  def test_examples_count_animals_command_help(self):
    """Test the count_animals command help in mod_example.py."""
    examples_path = Path(__file__).parent.parent / "mod_example.py"
    result = subprocess.run(
      [sys.executable, str(examples_path), "count-animals", "--help"],
      capture_output=True,
      text=True,
      timeout=10
    )

    assert result.returncode == 0
    assert "count" in result.stdout
    assert "animal" in result.stdout


class TestClassExample:
  """Test cases for the cls_example.py file."""

  def test_class_example_help(self):
    """Test that cls_example.py shows help without errors."""
    examples_path = Path(__file__).parent.parent / "cls_example.py"
    result = subprocess.run(
      [sys.executable, str(examples_path), "--help"],
      capture_output=True,
      text=True,
      timeout=10
    )

    assert result.returncode == 0
    assert "Usage:" in result.stdout or "usage:" in result.stdout
    assert "Enhanced data processing utility" in result.stdout

  def test_class_example_process_file(self):
    """Test the file-operations process-single command group in cls_example.py."""
    examples_path = Path(__file__).parent.parent / "cls_example.py"
    result = subprocess.run(
      [sys.executable, str(examples_path), "file-operations", "process-single", "--input-file", "test.txt"],
      capture_output=True,
      text=True,
      timeout=10
    )

    assert result.returncode == 0
    assert "Processing file: test.txt" in result.stdout

  def test_class_example_config_command(self):
    """Test config-management set-default-mode command group in cls_example.py."""
    examples_path = Path(__file__).parent.parent / "cls_example.py"
    result = subprocess.run(
      [sys.executable, str(examples_path), "config-management", "set-default-mode", "--mode", "FAST"],
      capture_output=True,
      text=True,
      timeout=10
    )

    assert result.returncode == 0
    assert "Setting default processing mode to: fast" in result.stdout

  def test_class_example_config_help(self):
    """Test that config management commands are listed in main help."""
    examples_path = Path(__file__).parent.parent / "cls_example.py"
    result = subprocess.run(
      [sys.executable, str(examples_path), "--help"],
      capture_output=True,
      text=True,
      timeout=10
    )

    assert result.returncode == 0
    assert "config-management" in result.stdout  # Command group should appear
    assert "set-default-mode" in result.stdout   # Command group command should appear

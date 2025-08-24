#!/usr/bin/env python
# Enhanced examples demonstrating auto-cli-py with docstring integration.
import enum
import sys
from pathlib import Path

from auto_cli.cli import CLI


class LogLevel(enum.Enum):
  """Logging level options for output verbosity."""
  DEBUG = "debug"
  INFO = "info"
  WARNING = "warning"
  ERROR = "error"


class AnimalType(enum.Enum):
  """Different types of animals for counting."""
  ANT = 1
  BEE = 2
  CAT = 3
  DOG = 4


def foo():
  """Simple greeting function with no parameters."""
  print("FOO!")


def hello(name: str = "World", count: int = 1, excited: bool = False):
  """Greet someone with configurable enthusiasm.

  :param name: Name of the person to greet
  :param count: Number of times to repeat the greeting
  :param excited: Add exclamation marks for enthusiasm
  """
  suffix = "!!!" if excited else "."
  for _ in range(count):
    print(f"Hello, {name}{suffix}")


def train(
    data_dir: str = "./data/",
    initial_learning_rate: float = 0.0001,
    seed: int = 2112,
    batch_size: int = 512,
    epochs: int = 20,
    use_gpu: bool = False
):
  """Train a machine learning model with specified parameters.

  :param data_dir: Directory containing training data files
  :param initial_learning_rate: Starting learning rate for optimization
  :param seed: Random seed for reproducible results
  :param batch_size: Number of samples per training batch
  :param epochs: Number of complete passes through the training data
  :param use_gpu: Enable GPU acceleration if available
  """
  gpu_status = "GPU" if use_gpu else "CPU"
  params = {
    "Data directory": data_dir,
    "Learning rate": initial_learning_rate,
    "Random seed": seed,
    "Batch size": batch_size,
    "Epochs": epochs
  }
  print(f"Training model on {gpu_status}:")
  print('\n'.join(f"  {k}: {v}" for k, v in params.items()))


def count_animals(count: int = 20, animal: AnimalType = AnimalType.BEE):
  """Count animals of a specific type.

  :param count: Number of animals to count
  :param animal: Type of animal to count from the available options
  """
  print(f"Counting {count} {animal.name.lower()}s!")
  return count


def advanced_demo(
    text: str,
    iterations: int = 1,
    config_file: Path | None = None,
    debug_mode: bool = False
):
  """Demonstrate advanced parameter handling and edge cases.

  This function showcases how the CLI handles various parameter types
  including required parameters, optional files, and boolean flags.

  :param text: Required text input for processing
  :param iterations: Number of times to process the input text
  :param config_file: Optional configuration file to load settings from
  :param debug_mode: Enable detailed debug output during processing
  """
  print(f"Processing text: '{text}'")
  print(f"Iterations: {iterations}")

  if config_file:
    if config_file.exists():
      print(f"Loading config from: {config_file}")
    else:
      print(f"Warning: Config file not found: {config_file}")

  if debug_mode:
    print("DEBUG: Advanced demo function called")
    print(f"DEBUG: Text length: {len(text)} characters")

  # Simulate processing
  for i in range(iterations):
    if debug_mode:
      print(f"DEBUG: Processing iteration {i + 1}/{iterations}")
    result = text.upper() if i % 2 == 0 else text.lower()
    print(f"Result {i + 1}: {result}")


# Database operations (converted from command groups to flat commands)
def create_database(
    name: str,
    engine: str = "postgres",
    host: str = "localhost",
    port: int = 5432,
    encrypted: bool = False
):
  """Create a new database instance.

  :param name: Name of the database to create
  :param engine: Database engine type (sqlite, postgres, mysql)
  :param host: Database host address
  :param port: Database port number
  :param encrypted: Enable database encryption
  """
  encryption_status = "encrypted" if encrypted else "unencrypted"
  print(f"Creating {encryption_status} {engine} database '{name}'")
  print(f"Host: {host}:{port}")
  print("✓ Database created successfully")


def migrate_database(
    direction: str = "up",
    steps: int = 1,
    dry_run: bool = False,
    force: bool = False
):
  """Run database migrations.

  :param direction: Migration direction (up or down)
  :param steps: Number of migration steps to execute
  :param dry_run: Show what would be migrated without applying changes
  :param force: Force migration even if conflicts exist
  """
  action = "Would migrate" if dry_run else "Migrating"
  force_text = " (forced)" if force else ""
  print(f"{action} {steps} step(s) {direction}{force_text}")

  if not dry_run:
    for i in range(steps):
      print(f"  Running migration {i + 1}/{steps}...")
    print("✓ Migrations completed")


def backup_database(
    file_path: Path,
    compress: bool = True,
    exclude_tables: str = ""
):
  """Backup database to file.

  :param file_path: Path to backup file
  :param compress: Compress backup files
  :param exclude_tables: Comma-separated list of tables to exclude from backup
  """
  backup_type = "compressed" if compress else "uncompressed"
  print(f"Creating {backup_type} backup at: {file_path}")

  if exclude_tables:
    excluded = exclude_tables.split(',')
    print(f"Excluding tables: {', '.join(excluded)}")

  print("✓ Backup completed successfully")


def restore_database(
    file_path: Path
):
  """Restore database from backup file.

  :param file_path: Path to backup file
  """
  print(f"Restoring database from: {file_path}")
  print("✓ Restore completed successfully")


# Admin operations (converted from nested command groups to flat commands)
def reset_user_password(username: str, notify_user: bool = True):
  """Reset a user's password (admin operation).

  :param username: Username whose password to reset
  :param notify_user: Send notification email to user
  """
  print(f"🔑 Admin operation: Resetting password for user '{username}'")
  if notify_user:
    print("📧 Sending password reset notification")
  print("✓ Password reset completed")


def set_maintenance_mode(enable: bool, message: str = "System maintenance in progress"):
  """Enable or disable system maintenance mode.

  :param enable: Enable (True) or disable (False) maintenance mode
  :param message: Message to display to users during maintenance
  """
  action = "Enabling" if enable else "Disabling"
  print(f"🔧 {action} system maintenance mode")
  if enable:
    print(f"📢 Message: '{message}'")
  print("✓ Maintenance mode updated")


def completion_demo(config_file: str = "config.json", output_dir: str = "./output"):
  """Demonstrate completion for file paths and configuration.

  :param config_file: Configuration file path (demonstrates file completion)
  :param output_dir: Output directory path (demonstrates directory completion)
  """
  print(f"🔧 Using config file: {config_file}")
  print(f"📂 Output directory: {output_dir}")
  print("✨ This command demonstrates file/directory path completion!")
  print("💡 Try: python mod_example.py completion-demo --config-file <TAB>")
  print("💡 Try: python mod_example.py completion-demo --output-dir <TAB>")


if __name__ == '__main__':
  # Import theme functionality
  from auto_cli.theme import create_default_theme

  # Create CLI with colored theme and completion enabled
  theme = create_default_theme()
  cli = CLI(
    sys.modules[__name__],
    title="Enhanced CLI - Module-based flat commands",
    theme=theme,
    enable_completion=True  # Enable shell completion
  )

  # Run the CLI and exit with appropriate code
  result = cli.run()
  sys.exit(result if isinstance(result, int) else 0)

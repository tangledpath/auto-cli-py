# 🗂️ Module-Based CLI Guide

[← Back to User Guide](index.md) | [↑ Documentation Hub](../help.md) | [Class CLI Guide →](class-cli.md)

## Table of Contents
- [Overview](#overview)
- [When to Use Module-Based CLI](#when-to-use-module-based-cli)
- [Getting Started](#getting-started)
- [Function Design](#function-design)
- [Creating Your CLI](#creating-your-cli)
- [Hierarchical Commands](#hierarchical-commands)
- [Advanced Features](#advanced-features)
- [Complete Example](#complete-example)
- [Best Practices](#best-practices)
- [Testing](#testing)
- [Migration Guide](#migration-guide)
- [See Also](#see-also)

## Overview

Module-based CLI generation creates command-line interfaces from functions defined in a Python module. This is the original and most straightforward approach in auto-cli-py, perfect for scripts, utilities, and functional programming styles.

```python
# Your functions become CLI commands automatically!
def process_data(input_file: str, output_dir: str = "./output", verbose: bool = False):
    """Process data from input file."""
    print(f"Processing {input_file} -> {output_dir}")
```

## When to Use Module-Based CLI

Module-based CLI is ideal when:

✅ **You have existing functions** that you want to expose as CLI commands  
✅ **Your code follows functional programming** patterns  
✅ **You're building command-line scripts** or utilities  
✅ **Operations are stateless** and independent  
✅ **You prefer simple, flat organization** of commands  
✅ **You're migrating from argparse or click** with existing functions  

Consider class-based CLI instead if:
- You need to maintain state between commands
- Your operations are naturally grouped into a service or manager
- You have complex initialization requirements
- You're building an object-oriented application

## Getting Started

### Basic Setup

1. **Import required modules:**
```python
import sys
from auto_cli.cli import CLI
```

2. **Define your functions with type hints:**
```python
def greet(name: str, times: int = 1, excited: bool = False):
    """Greet someone multiple times.
    
    :param name: Person's name to greet
    :param times: Number of greetings
    :param excited: Add excitement to greeting
    """
    greeting = f"Hello, {name}{'!' if excited else '.'}"
    for _ in range(times):
        print(greeting)
```

3. **Create and run the CLI:**
```python
if __name__ == '__main__':
    cli = CLI.from_module(
        sys.modules[__name__],
        title="My Greeting CLI"
    )
    cli.run()
```

4. **Use your CLI:**
```bash
$ python greet.py greet --name Alice --times 3 --excited
Hello, Alice!
Hello, Alice!
Hello, Alice!
```

## Function Design

### Type Annotations

Auto-cli-py uses type annotations to determine argument types:

```python
def example_types(
    text: str,                    # String argument
    count: int = 10,              # Integer with default
    ratio: float = 0.5,           # Float with default
    enabled: bool = False,        # Boolean flag
    path: Path = Path("./data")   # Path type
):
    """Demonstrate various parameter types."""
    pass
```

### Enum Support

Use enums for choice parameters:

```python
from enum import Enum

class LogLevel(Enum):
    DEBUG = "debug"
    INFO = "info"
    ERROR = "error"

def configure_logging(level: LogLevel = LogLevel.INFO):
    """Set the logging level."""
    print(f"Log level set to: {level.value}")
```

### Optional Parameters

Use Optional or Union types:

```python
from typing import Optional

def process_file(
    input_file: str,
    output_file: Optional[str] = None,
    encoding: str = "utf-8"
):
    """Process a file with optional output."""
    output = output_file or f"{input_file}.processed"
    print(f"Processing {input_file} -> {output}")
```

### Docstring Integration

Auto-cli-py extracts help text from docstrings:

```python
def deploy(
    environment: str,
    version: str = "latest",
    dry_run: bool = False
):
    """Deploy application to specified environment.
    
    This function handles the deployment process including
    validation, backup, and rollout.
    
    :param environment: Target environment (dev, staging, prod)
    :param version: Version tag or 'latest'
    :param dry_run: Simulate deployment without changes
    """
    action = "Would deploy" if dry_run else "Deploying"
    print(f"{action} version {version} to {environment}")
```

## Creating Your CLI

### Basic CLI Creation

```python
# Simple CLI with all module functions
cli = CLI.from_module(
    sys.modules[__name__],
    title="My Tool"
)
cli.run()
```

### With Function Filter

Control which functions become commands:

```python
def is_public_command(func_name: str, func: callable) -> bool:
    """Include only public functions (not starting with _)."""
    return not func_name.startswith('_')

cli = CLI.from_module(
    sys.modules[__name__],
    title="My Tool",
    function_filter=is_public_command
)
```

### With Theme Support

Add beautiful colored output:

```python
from auto_cli.theme import create_default_theme

theme = create_default_theme()
cli = CLI.from_module(
    sys.modules[__name__],
    title="My Tool",
    theme=theme,
    theme_tuner=True  # Add theme tuning command
)
```

### With Shell Completion

Enable tab completion:

```python
cli = CLI.from_module(
    sys.modules[__name__],
    title="My Tool",
    enable_completion=True
)
```

## Hierarchical Commands

Use double underscores to create command hierarchies:

```python
# Database commands group
@CLI.CommandGroup("Database operations")
def db__create(name: str, type: str = "postgres"):
    """Create a new database."""
    print(f"Creating {type} database: {name}")

def db__backup(name: str, output: str = "./backups"):
    """Backup a database."""
    print(f"Backing up {name} to {output}")

def db__restore(name: str, backup_file: str):
    """Restore database from backup."""
    print(f"Restoring {name} from {backup_file}")

# User management commands
@CLI.CommandGroup("User management operations")  
def user__create(username: str, email: str, admin: bool = False):
    """Create a new user account."""
    role = "admin" if admin else "user"
    print(f"Creating {role}: {username} ({email})")

def user__list(active_only: bool = True):
    """List all users."""
    filter_text = "active" if active_only else "all"
    print(f"Listing {filter_text} users...")

# Multi-level hierarchy
def admin__system__restart(force: bool = False):
    """Restart the system."""
    mode = "forced" if force else "graceful"
    print(f"Performing {mode} system restart...")
```

Usage:
```bash
$ python tool.py db create myapp
$ python tool.py user create alice alice@example.com --admin
$ python tool.py admin system restart --force
```

## Advanced Features

### Command Groups with Decorators

Add descriptions to command groups:

```python
@CLI.CommandGroup("File operations and management")
def file__compress(input_path: str, output: str = None):
    """Compress files or directories."""
    output = output or f"{input_path}.zip"
    print(f"Compressing {input_path} -> {output}")
```

### Complex Parameter Types

```python
from pathlib import Path
from typing import List, Optional

def analyze_logs(
    log_files: List[str],
    pattern: Optional[str] = None,
    output_format: str = "json",
    max_results: int = 100
):
    """Analyze multiple log files.
    
    :param log_files: List of log files to analyze
    :param pattern: Search pattern (regex)
    :param output_format: Output format (json, csv, table)
    :param max_results: Maximum results to return
    """
    print(f"Analyzing {len(log_files)} files")
    if pattern:
        print(f"Searching for: {pattern}")
    print(f"Output format: {output_format}")
```

### Function Metadata

Use function attributes for additional configuration:

```python
def dangerous_operation(confirm: bool = False):
    """Perform a dangerous operation."""
    if not confirm:
        print("Operation cancelled. Use --confirm to proceed.")
        return 1
    print("Executing dangerous operation...")
    return 0

# Add custom metadata
dangerous_operation.require_confirmation = True
```

## Complete Example

Here's a complete example showing various features:

```python
#!/usr/bin/env python
"""File management CLI tool."""

import sys
from pathlib import Path
from enum import Enum
from typing import Optional, List
from auto_cli.cli import CLI
from auto_cli.theme import create_default_theme

class CompressionType(Enum):
    ZIP = "zip"
    TAR = "tar"
    GZIP = "gzip"

class SortOrder(Enum):
    NAME = "name"
    SIZE = "size"
    DATE = "date"

# Basic file operations
def list_files(
    directory: str = ".",
    pattern: str = "*",
    recursive: bool = False,
    sort_by: SortOrder = SortOrder.NAME
):
    """List files in a directory.
    
    :param directory: Directory to list
    :param pattern: File pattern to match
    :param recursive: Include subdirectories
    :param sort_by: Sort order for results
    """
    path = Path(directory)
    search_pattern = f"**/{pattern}" if recursive else pattern
    
    print(f"Listing files in {path.absolute()}")
    print(f"Pattern: {pattern}")
    print(f"Sort by: {sort_by.value}")
    
    files = list(path.glob(search_pattern))
    print(f"Found {len(files)} files")

def copy_file(
    source: str,
    destination: str,
    overwrite: bool = False,
    preserve_metadata: bool = True
):
    """Copy a file to destination.
    
    :param source: Source file path
    :param destination: Destination path
    :param overwrite: Overwrite if exists
    :param preserve_metadata: Preserve file metadata
    """
    action = "Would copy" if not overwrite else "Copying"
    metadata = "with" if preserve_metadata else "without"
    print(f"{action} {source} -> {destination} ({metadata} metadata)")

# Archive operations
@CLI.CommandGroup("Archive and compression operations")
def archive__create(
    files: List[str],
    output: str,
    compression: CompressionType = CompressionType.ZIP,
    level: int = 6
):
    """Create an archive from files.
    
    :param files: Files to archive
    :param output: Output archive path
    :param compression: Compression type
    :param level: Compression level (1-9)
    """
    print(f"Creating {compression.value} archive: {output}")
    print(f"Compression level: {level}")
    print(f"Adding {len(files)} files:")
    for f in files:
        print(f"  - {f}")

def archive__extract(
    archive: str,
    destination: str = ".",
    files: Optional[List[str]] = None
):
    """Extract files from archive.
    
    :param archive: Archive file path
    :param destination: Extract destination
    :param files: Specific files to extract (all if none)
    """
    print(f"Extracting {archive} -> {destination}")
    if files:
        print(f"Extracting only: {', '.join(files)}")
    else:
        print("Extracting all files")

# Sync operations
@CLI.CommandGroup("Synchronization operations")
def sync__folders(
    source: str,
    destination: str,
    delete: bool = False,
    dry_run: bool = False
):
    """Synchronize two folders.
    
    :param source: Source folder
    :param destination: Destination folder
    :param delete: Delete files not in source
    :param dry_run: Show what would be done
    """
    mode = "Simulating" if dry_run else "Executing"
    delete_mode = "with deletion" if delete else "without deletion"
    print(f"{mode} sync: {source} -> {destination} ({delete_mode})")

# Admin operations
def admin__cleanup(
    older_than_days: int = 30,
    pattern: str = "*.tmp",
    force: bool = False
):
    """Clean up old temporary files.
    
    :param older_than_days: Age threshold in days
    :param pattern: File pattern to match
    :param force: Skip confirmation
    """
    if not force:
        print(f"Would delete files matching '{pattern}' older than {older_than_days} days")
        print("Use --force to actually delete")
    else:
        print(f"Deleting files matching '{pattern}' older than {older_than_days} days")

if __name__ == '__main__':
    # Create CLI with all features
    theme = create_default_theme()
    cli = CLI.from_module(
        sys.modules[__name__],
        title="File Manager - Professional file management tool",
        theme=theme,
        theme_tuner=True,
        enable_completion=True
    )
    
    # Run CLI
    result = cli.run()
    sys.exit(result if isinstance(result, int) else 0)
```

## Best Practices

### 1. Function Naming
- Use clear, action-oriented names
- Use underscores for word separation
- Use double underscores for hierarchies
- Avoid abbreviations

### 2. Parameter Design
- Always use type annotations
- Provide sensible defaults
- Use enums for choices
- Keep required parameters minimal

### 3. Documentation
- Write clear docstrings
- Document all parameters
- Include usage examples
- Explain side effects

### 4. Error Handling
```python
def safe_operation(file: str, force: bool = False):
    """Perform operation with error handling."""
    if not Path(file).exists() and not force:
        print(f"Error: File not found: {file}")
        return 1  # Return error code
    
    try:
        # Perform operation
        print(f"Processing {file}")
        return 0  # Success
    except Exception as e:
        print(f"Error: {e}")
        return 2  # Error code
```

### 5. Module Organization
```python
# constants.py
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3

# utils.py
def validate_input(data: str) -> bool:
    """Validate input data."""
    return len(data) > 0

# operations.py
def process(data: str, timeout: int = DEFAULT_TIMEOUT):
    """Process data with timeout."""
    if not validate_input(data):
        return 1
    print(f"Processing with timeout: {timeout}s")
    return 0

# cli.py
if __name__ == '__main__':
    import operations
    cli = CLI.from_module(operations, title="Processor")
    cli.run()
```

## Testing

### Unit Testing Functions

```python
# test_functions.py
import pytest
from mymodule import greet, process_file

def test_greet_basic():
    """Test basic greeting."""
    # Function can be tested independently
    result = greet("Alice", times=1, excited=False)
    assert result == 0  # Check return code

def test_process_file_missing():
    """Test processing missing file."""
    result = process_file("nonexistent.txt")
    assert result == 1  # Error code
```

### Integration Testing CLI

```python
# test_cli.py
import subprocess
import sys

def test_cli_help():
    """Test CLI help display."""
    result = subprocess.run(
        [sys.executable, "mycli.py", "--help"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "usage:" in result.stdout

def test_cli_command():
    """Test CLI command execution."""
    result = subprocess.run(
        [sys.executable, "mycli.py", "greet", "--name", "Test"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Hello, Test" in result.stdout
```

## Migration Guide

### From argparse

**Before (argparse):**
```python
import argparse

def main():
    parser = argparse.ArgumentParser(description="My tool")
    parser.add_argument("--name", type=str, default="World")
    parser.add_argument("--count", type=int, default=1)
    parser.add_argument("--excited", action="store_true")
    
    args = parser.parse_args()
    
    for _ in range(args.count):
        greeting = f"Hello, {args.name}{'!' if args.excited else '.'}"
        print(greeting)

if __name__ == "__main__":
    main()
```

**After (auto-cli-py):**
```python
from auto_cli.cli import CLI
import sys

def greet(name: str = "World", count: int = 1, excited: bool = False):
    """Greet someone multiple times."""
    for _ in range(count):
        greeting = f"Hello, {name}{'!' if excited else '.'}"
        print(greeting)

if __name__ == "__main__":
    cli = CLI.from_module(sys.modules[__name__], title="My tool")
    cli.run()
```

### From click

**Before (click):**
```python
import click

@click.command()
@click.option('--name', default='World', help='Name to greet')
@click.option('--count', default=1, help='Number of greetings')
@click.option('--excited', is_flag=True, help='Add excitement')
def greet(name, count, excited):
    """Greet someone multiple times."""
    for _ in range(count):
        greeting = f"Hello, {name}{'!' if excited else '.'}"
        click.echo(greeting)

if __name__ == '__main__':
    greet()
```

**After (auto-cli-py):**
```python
from auto_cli.cli import CLI
import sys

def greet(name: str = "World", count: int = 1, excited: bool = False):
    """Greet someone multiple times.
    
    :param name: Name to greet
    :param count: Number of greetings  
    :param excited: Add excitement
    """
    for _ in range(count):
        greeting = f"Hello, {name}{'!' if excited else '.'}"
        print(greeting)

if __name__ == "__main__":
    cli = CLI.from_module(sys.modules[__name__], title="Greeter")
    cli.run()
```

## See Also

- [Class-Based CLI Guide](class-cli.md) - Alternative approach using classes
- [Mode Comparison](mode-comparison.md) - Detailed comparison of both modes
- [Type Annotations](../features/type-annotations.md) - Supported types
- [Examples](../guides/examples.md) - More real-world examples
- [API Reference](../reference/api.md) - Complete API documentation

---

**Navigation**: [← User Guide](index.md) | [↑ Documentation Hub](../help.md) | [Class CLI Guide →](class-cli.md)
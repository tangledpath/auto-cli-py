# Choosing Your CLI Mode

[← Back to Getting Started](index.md) | [↑ Documentation Hub](../help.md)

## Overview

Auto-CLI-Py offers two distinct modes for creating command-line interfaces. This guide helps you choose the right approach for your project.

## Quick Decision Guide

### Choose **Module-based CLI** if:
- ✅ You have existing functions to expose as commands
- ✅ Your operations are stateless and independent
- ✅ You prefer functional programming style
- ✅ You're building simple scripts or utilities
- ✅ You want the quickest path to a working CLI

### Choose **Class-based CLI** if:
- ✅ You need to maintain state between commands
- ✅ Your operations share configuration or resources
- ✅ You prefer object-oriented design
- ✅ You're building complex applications
- ✅ You need initialization/cleanup logic

## Mode Comparison

| Feature | Module-based | Class-based |
|---------|--------------|-------------|
| **Setup complexity** | Simple | Moderate |
| **State management** | No built-in state | Instance maintains state |
| **Code organization** | Functions in module | Methods in class |
| **Best for** | Scripts, utilities | Applications, services |
| **Command structure** | Flat commands | Flat commands + inner classes |
| **Initialization** | None required | Constructor with defaults |

## Examples

### Module-based Example
```python
# file_utils.py
from auto_cli import CLI
import sys

def compress_file(input_file: str, output_file: str = None) -> None:
    """Compress a file."""
    output = output_file or f"{input_file}.gz"
    print(f"Compressing {input_file} -> {output}")

def extract_file(archive: str, destination: str = ".") -> None:
    """Extract an archive."""
    print(f"Extracting {archive} -> {destination}")

if __name__ == '__main__':
    cli = CLI(sys.modules[__name__], title="File Utilities")
    cli.display()
```

### Class-based Example
```python
# database_manager.py
from auto_cli import CLI

class DatabaseManager:
    """Database management tool."""
    
    def __init__(self, host: str = "localhost", port: int = 5432):
        """Initialize with connection settings."""
        self.host = host
        self.port = port
        self.connection = None
    
    def connect(self, database: str) -> None:
        """Connect to a database."""
        print(f"Connecting to {database} at {self.host}:{self.port}")
        self.connection = f"{self.host}:{self.port}/{database}"
    
    def backup(self, output: str = "backup.sql") -> None:
        """Backup the connected database."""
        if not self.connection:
            print("Error: Not connected to any database")
            return
        print(f"Backing up {self.connection} to {output}")

if __name__ == '__main__':
    cli = CLI(DatabaseManager)
    cli.display()
```

## Next Steps

Once you've chosen your mode:

- **Module-based**: Continue to [Module CLI Quick Start](module-cli.md)
- **Class-based**: Continue to [Class CLI Quick Start](class-cli.md)

For detailed documentation:
- [Complete Module CLI Guide](../user-guide/module-cli.md)
- [Complete Class CLI Guide](../user-guide/class-cli.md)

---

**Navigation**: [← Installation](installation.md) | [Quick Start →](quick-start.md)
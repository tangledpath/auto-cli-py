# Class CLI Quick Start

[← Back to Getting Started](index.md) | [↑ Documentation Hub](../help.md)

## Overview

Class-based CLI creates commands from methods in a Python class. This approach is perfect for applications that need to maintain state between commands.

## Basic Example

```python
# calculator_cli.py
from auto_cli import CLI

class Calculator:
    """A simple calculator that remembers the last result."""
    
    def __init__(self, initial_value: float = 0.0):
        """Initialize calculator with optional starting value."""
        self.value = initial_value
        self.history = []
    
    def add(self, number: float) -> None:
        """Add a number to the current value."""
        old_value = self.value
        self.value += number
        self.history.append(f"{old_value} + {number} = {self.value}")
        print(f"Result: {self.value}")
    
    def subtract(self, number: float) -> None:
        """Subtract a number from the current value."""
        old_value = self.value
        self.value -= number
        self.history.append(f"{old_value} - {number} = {self.value}")
        print(f"Result: {self.value}")
    
    def show(self) -> None:
        """Show the current value."""
        print(f"Current value: {self.value}")
    
    def history_list(self) -> None:
        """Show calculation history."""
        if not self.history:
            print("No calculations yet")
        else:
            print("History:")
            for entry in self.history:
                print(f"  {entry}")

if __name__ == '__main__':
    cli = CLI(Calculator, title="Calculator CLI")
    cli.display()
```

## Running Your CLI

```bash
# Show help
python calculator_cli.py --help

# Use with initial value
python calculator_cli.py --initial-value 100 add --number 50
python calculator_cli.py --initial-value 100 show

# Chain operations (each runs independently)
python calculator_cli.py add --number 10
python calculator_cli.py subtract --number 5
python calculator_cli.py history-list
```

## Key Requirements

### 1. Constructor Defaults Required
All constructor parameters must have default values:
```python
# ✅ Good - all parameters have defaults
def __init__(self, config_file: str = "config.json", debug: bool = False):
    pass

# ❌ Bad - missing defaults
def __init__(self, config_file: str):
    pass
```

### 2. Method Requirements
- Must have type annotations
- Can't start with underscore `_`
- Should not require `self` parameter in CLI

### 3. State Management
The class instance persists across the single command execution:
```python
class StatefulApp:
    def __init__(self, db_path: str = "app.db"):
        self.db = self.connect_db(db_path)
        self.cache = {}
    
    def process(self, data: str) -> None:
        """Process data using persistent connection."""
        # Uses self.db and self.cache
        pass
```

## Inner Classes Pattern

For better organization, use inner classes (creates flat commands with double-dash notation):

```python
class ProjectManager:
    """Project management CLI."""
    
    def __init__(self, workspace: str = "./projects"):
        self.workspace = workspace
    
    class FileOperations:
        """File-related commands."""
        
        def create(self, name: str, template: str = "default") -> None:
            """Create a new file."""
            print(f"Creating {name} from template {template}")
    
    class GitOperations:
        """Git-related commands."""
        
        def commit(self, message: str) -> None:
            """Create a git commit."""
            print(f"Committing with message: {message}")

# Usage:
# python project_mgr.py file-operations--create --name "README.md"
# python project_mgr.py git-operations--commit --message "Initial commit"
```

## Next Steps

- For comprehensive documentation, see the [Complete Class CLI Guide](../user-guide/class-cli.md)
- Learn about [Inner Classes Pattern](../user-guide/inner-classes.md) for complex CLIs
- Compare with [Module CLI Quick Start](module-cli.md)

---

**Navigation**: [← Module CLI Quick Start](module-cli.md) | [Basic Usage →](basic-usage.md)
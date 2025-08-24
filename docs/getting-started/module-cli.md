# Module CLI Quick Start

[← Back to Getting Started](index.md) | [↑ Documentation Hub](../help.md)

## Overview

Module-based CLI creates commands from functions in a Python module. This is the simplest way to build a CLI with Auto-CLI-Py.

## Basic Example

```python
# hello_cli.py
from auto_cli import CLI
import sys

def hello(name: str = "World", excited: bool = False) -> None:
    """Say hello to someone."""
    greeting = f"Hello, {name}!"
    if excited:
        greeting += " 🎉"
    print(greeting)

def goodbye(name: str = "World", formal: bool = False) -> None:
    """Say goodbye to someone."""
    if formal:
        print(f"Farewell, {name}. Until we meet again.")
    else:
        print(f"Bye, {name}!")

if __name__ == '__main__':
    cli = CLI(sys.modules[__name__], title="Greeting CLI")
    cli.display()
```

## Running Your CLI

```bash
# Show help
python hello_cli.py --help

# Use commands
python hello_cli.py hello --name Alice --excited
python hello_cli.py goodbye --name Bob --formal
```

## Key Requirements

### 1. Type Annotations Required
All function parameters must have type annotations:
```python
# ✅ Good
def process(file: str, count: int = 10) -> None:
    pass

# ❌ Bad - missing annotations
def process(file, count=10):
    pass
```

### 2. Supported Types
- `str` - String values
- `int` - Integer numbers
- `float` - Decimal numbers
- `bool` - Boolean flags (no value needed)
- `List[str]` - Multiple string values
- `Enum` - Choice from predefined options

### 3. Function Naming
- Use descriptive names
- Functions starting with `_` are ignored
- Use snake_case naming

## Adding More Features

### Using Enums for Choices
```python
from enum import Enum

class Color(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"

def paint(item: str, color: Color = Color.BLUE) -> None:
    """Paint an item with a color."""
    print(f"Painting {item} {color.value}")
```

### Multiple Parameters
```python
from typing import List

def process_files(
    files: List[str],
    output_dir: str = "./output",
    verbose: bool = False
) -> None:
    """Process multiple files."""
    print(f"Processing {len(files)} files")
    if verbose:
        for file in files:
            print(f"  - {file}")
```

## Next Steps

- For comprehensive documentation, see the [Complete Module CLI Guide](../user-guide/module-cli.md)
- Try the [Class CLI Quick Start](class-cli.md) for stateful applications
- Explore [Type Annotations](../features/type-annotations.md) in detail

---

**Navigation**: [← Choosing CLI Mode](choosing-cli-mode.md) | [Class CLI Quick Start →](class-cli.md)
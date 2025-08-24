# API Reference

[↑ Documentation Hub](../help.md)

Complete API documentation and technical reference for Auto-CLI-Py.

## Reference Documentation

### 📚 [Complete API](api.md)
Full API documentation for all public interfaces.
- CLI class methods and properties
- Factory methods (from_module, from_class)
- Configuration options
- Return types and exceptions

### 🏗️ [CLI Class](cli-class.md)
Detailed documentation of the CLI class.
- Constructor parameters
- Instance methods
- Class methods
- Properties and attributes
- Internal behavior

### 🔤 [Parameter Types](parameter-types.md)
Complete guide to supported parameter types.
- Type mapping table
- Custom type handlers
- Collection types
- Optional and Union types
- Type conversion rules

## Quick Reference

### CLI Creation

**Module-based CLI**
```python
from auto_cli import CLI
import sys

cli = CLI(
    sys.modules[__name__],
    title="My CLI",
    theme_name="universal",
    no_color=False,
    completion=True
)
cli.display()
```

**Class-based CLI**
```python
from auto_cli import CLI

cli = CLI(
    MyClass,
    title="My CLI",
    theme_name="colorful",
    function_opts={
        'method_name': {
            'description': 'Custom description',
            'hidden': False
        }
    }
)
cli.display()
```

### Common Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `title` | str | None | CLI title (from docstring if None) |
| `theme_name` | str | "universal" | Theme name ("colorful" or "universal") |
| `no_color` | bool | False | Disable colored output |
| `completion` | bool | True | Enable shell completion |
| `function_opts` | dict | None | Per-function/method configuration |

### Type Mappings

| Python Type | CLI Argument | Example |
|-------------|--------------|---------|
| `str` | String value | `--name "John"` |
| `int` | Integer value | `--count 42` |
| `float` | Float value | `--rate 3.14` |
| `bool` | Flag (no value) | `--verbose` |
| `List[str]` | Multiple values | `--files a.txt b.txt` |
| `Enum` | Choice from enum | `--level INFO` |
| `Path` | Path value | `--config /etc/app.conf` |

### Method Signatures

**Factory Methods**
```python
@classmethod
def from_module(
    cls,
    module,
    title: Optional[str] = None,
    **kwargs
) -> 'CLI':
    """Create CLI from module functions."""

@classmethod  
def from_class(
    cls,
    class_type: Type,
    title: Optional[str] = None,
    **kwargs
) -> 'CLI':
    """Create CLI from class methods."""
```

**Instance Methods**
```python
def display(self) -> Optional[int]:
    """Display CLI interface and execute commands."""

def run(self) -> Optional[int]:
    """Alias for display() method."""

def add_command(
    self,
    name: str,
    function: Callable,
    description: Optional[str] = None
) -> None:
    """Add a command to the CLI."""
```

## Architecture Overview

### Component Structure
```
auto_cli/
├── cli.py          # Main CLI class
├── __init__.py     # Package exports
├── theme.py        # Theme system
├── completion.py   # Shell completion
└── utils.py        # Helper functions
```

### Design Principles
- Zero configuration by default
- Type-driven interface generation
- Extensible and customizable
- Performance optimized
- Well-tested and documented

## Next Steps

- Explore the [Complete API](api.md)
- Understand the [CLI Class](cli-class.md)
- Review [Parameter Types](parameter-types.md)
- See [Examples](../guides/examples.md) for usage

---

**Need source code?** Visit [GitHub](https://github.com/tangledpath/auto-cli-py)
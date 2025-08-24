# API Reference

[← Back to Help](../help.md) | [🔧 Basic Usage](../getting-started/basic-usage.md)

## Table of Contents
- [CLI Class](#cli-class)
- [Factory Methods](#factory-methods)
- [Configuration Options](#configuration-options)
- [Function Options](#function-options)
- [Return Values](#return-values)
- [Exceptions](#exceptions)
- [Advanced Usage](#advanced-usage)

## CLI Class

The main `CLI` class provides the interface for creating command-line applications from your Python code.

```python
from auto_cli import CLI
```

### Factory Methods

#### `CLI.from_module()`

Create CLI from module functions (module-based approach).

```python
@classmethod
def from_module(
    cls,
    module: ModuleType,
    title: str = None,
    function_opts: Dict[str, Dict[str, Any]] = None,
    theme_name: str = "universal",
    no_color: bool = False,
    completion: bool = True
) -> CLI:
```

**Parameters:**
- **`module`** (`ModuleType`): The Python module containing functions to expose as CLI commands
- **`title`** (`str`, optional): CLI application title. If None, extracted from module docstring
- **`function_opts`** (`Dict[str, Dict[str, Any]]`, optional): Per-function configuration options
- **`theme_name`** (`str`): Built-in theme name ("universal" or "colorful")
- **`no_color`** (`bool`): Disable colored output
- **`completion`** (`bool`): Enable shell completion support

**Returns:** `CLI` instance

**Example:**
```python
import sys
from auto_cli import CLI

def greet(name: str = "World") -> None:
    """Greet someone by name."""
    print(f"Hello, {name}!")

cli = CLI.from_module(
    sys.modules[__name__],
    title="Greeting CLI",
    theme_name="colorful"
)
cli.display()
```

#### `CLI.from_class()`

Create CLI from class methods (class-based approach).

```python
@classmethod
def from_class(
    cls,
    target_class: Type,
    title: str = None,
    function_opts: Dict[str, Dict[str, Any]] = None,
    theme_name: str = "universal",
    no_color: bool = False,
    completion: bool = True
) -> CLI:
```

**Parameters:**
- **`target_class`** (`Type`): The class containing methods to expose as CLI commands
- **`title`** (`str`, optional): CLI application title. If None, extracted from class docstring
- **`function_opts`** (`Dict[str, Dict[str, Any]]`, optional): Per-method configuration options
- **`theme_name`** (`str`): Built-in theme name ("universal" or "colorful")
- **`no_color`** (`bool`): Disable colored output
- **`completion`** (`bool`): Enable shell completion support

**Returns:** `CLI` instance

**Example:**
```python
from auto_cli import CLI

class TaskManager:
    """Task Management Application."""
    
    def __init__(self):
        self.tasks = []
    
    def add_task(self, title: str, priority: str = "medium") -> None:
        """Add a new task."""
        self.tasks.append({"title": title, "priority": priority})

cli = CLI.from_class(
    TaskManager,
    theme_name="colorful"
)
cli.display()
```

### Instance Methods

#### `display()`

Start the CLI application and process command-line arguments.

```python
def display(self) -> None:
```

This method:
1. Parses command-line arguments using `sys.argv`
2. Executes the appropriate function/method
3. Handles errors and displays help text
4. Exits the program with appropriate exit code

**Example:**
```python
if __name__ == '__main__':
    cli = CLI.from_module(sys.modules[__name__])
    cli.display()  # Starts CLI and handles all argument processing
```

## Configuration Options

### Theme Names

Built-in themes for customizing CLI appearance:

- **`"universal"`** (default): Balanced colors that work well across terminals
- **`"colorful"`**: More vibrant colors and styling

```python
# Universal theme (default)
cli = CLI.from_module(module, theme_name="universal")

# Colorful theme
cli = CLI.from_module(module, theme_name="colorful")

# Disable colors entirely
cli = CLI.from_module(module, no_color=True)
```

### Color Control

- **`no_color=False`** (default): Enable colored output
- **`no_color=True`**: Force disable all colors (overrides theme)

### Shell Completion

- **`completion=True`** (default): Enable shell completion support
- **`completion=False`**: Disable shell completion

Shell completion provides:
- Command name completion
- Parameter name completion  
- Enum value completion
- File path completion (where appropriate)

## Function Options

Configure individual functions/methods using the `function_opts` parameter:

```python
function_opts = {
    'function_name': {
        'description': 'Custom description text',
        'hidden': False,  # Hide from CLI command listing
        'aliases': ['alt1', 'alt2']  # Alternative command names (planned)
    }
}

cli = CLI.from_module(module, function_opts=function_opts)
```

### Function Option Keys

- **`description`** (`str`): Override the function's docstring description
- **`hidden`** (`bool`): Hide the function from CLI help (default: `False`)
- **`aliases`** (`List[str]`): Alternative names for the command (planned feature)

### Example Configuration

```python
def process_file(input_path: str, output_format: str = "json") -> None:
    """Process a file and convert to specified format."""
    pass

def internal_helper(data: str) -> None:
    """Internal helper function."""
    pass

function_opts = {
    'process_file': {
        'description': 'Advanced file processing with multiple output formats'
    },
    'internal_helper': {
        'hidden': True  # Hide from CLI
    }
}

cli = CLI.from_module(sys.modules[__name__], function_opts=function_opts)
```

## Return Values

### CLI Methods

All CLI factory methods return a `CLI` instance that provides:

- **`display()`**: Starts the CLI application
- Internal methods for argument parsing and execution (not part of public API)

### Function Execution

When CLI commands are executed:

- Functions with `-> None` return type: Exit code 0 on success
- Functions that raise exceptions: Exit code 1 with error message
- Functions with other return types: Return value is printed, exit code 0

## Exceptions

### Common Exceptions During CLI Creation

**`TypeError`**: Missing type annotations
```python
# This will raise TypeError
def bad_function(name):  # No type annotation
    pass

cli = CLI.from_module(sys.modules[__name__])  # Raises TypeError
```

**`AttributeError`**: Module/class doesn't contain expected functions/methods
```python
import empty_module
cli = CLI.from_module(empty_module)  # May raise AttributeError
```

### Runtime Exceptions

**`ValueError`**: Invalid argument values
```bash
# This generates ValueError for invalid int
python script.py process --count abc
```

**`FileNotFoundError`**: Missing required files (handled gracefully)
```python
def process_file(filename: str) -> None:
    with open(filename):  # User responsibility to handle
        pass
```

### Exception Handling

Auto-CLI-Py provides graceful error handling:

```python
def risky_function(value: int) -> None:
    """Function that might raise exceptions."""
    if value < 0:
        raise ValueError("Value must be positive")
    print(f"Processing: {value}")

# CLI automatically catches and displays user-friendly error messages
# Exit code 1 for exceptions, 0 for success
```

## Advanced Usage

### Dynamic CLI Creation

```python
def create_cli_dynamically(use_class_mode: bool = False):
    """Create CLI based on runtime conditions."""
    if use_class_mode:
        cli = CLI.from_class(MyAppClass)
    else:
        cli = CLI.from_module(sys.modules[__name__])
    return cli

if __name__ == '__main__':
    cli = create_cli_dynamically(use_class_mode=True)
    cli.display()
```

### Multiple CLI Instances

```python
def create_admin_cli():
    """CLI for admin functions."""
    return CLI.from_module(admin_module, title="Admin Tools")

def create_user_cli():
    """CLI for user functions."""  
    return CLI.from_module(user_module, title="User Tools")

if __name__ == '__main__':
    import sys
    if '--admin' in sys.argv:
        cli = create_admin_cli()
    else:
        cli = create_user_cli()
    cli.display()
```

### Custom Title Extraction

```python
class MyApp:
    """
    Advanced Application Suite
    
    This is a comprehensive application for advanced users.
    """
    
    def process(self, data: str) -> None:
        pass

# Title automatically extracted from class docstring:
# "Advanced Application Suite"
cli = CLI.from_class(MyApp)

# Override with custom title:
cli = CLI.from_class(MyApp, title="Custom App Name")
```

### Integration with External Libraries

```python
import logging
from pathlib import Path
from typing import List

# Configure logging before CLI creation
logging.basicConfig(level=logging.INFO)

def setup_logging(level: str = "INFO", log_file: str = None) -> None:
    """Configure application logging."""
    numeric_level = getattr(logging, level.upper())
    logging.getLogger().setLevel(numeric_level)
    
    if log_file:
        handler = logging.FileHandler(log_file)
        logging.getLogger().addHandler(handler)
    
    logging.info(f"Logging configured: level={level}, file={log_file}")

def process_files(
    input_paths: List[str],
    output_dir: str = "./output"
) -> None:
    """Process multiple files using Path objects."""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    for input_path in input_paths:
        path_obj = Path(input_path)
        logging.info(f"Processing: {path_obj}")
        # Processing logic here

if __name__ == '__main__':
    cli = CLI.from_module(sys.modules[__name__], title="File Processor")
    cli.display()
```

## Type Support Reference

| Python Type | CLI Behavior | Example |
|-------------|-------------|---------|
| `str` | String argument | `--name "value"` |
| `int` | Integer argument | `--count 42` |
| `float` | Float argument | `--rate 3.14` |
| `bool` | Flag (True/False) | `--verbose` or `--no-verbose` |
| `List[str]` | Multiple values | `--files f1.txt f2.txt` |
| `List[int]` | Multiple integers | `--numbers 1 2 3` |
| `Optional[T]` | Optional parameter | Can be omitted |
| `Union[str, int]` | Type conversion | Tries int, falls back to str |
| `Enum` | Choice parameter | `--level {debug,info,error}` |
| `Path` | Path object | `--dir /path/to/directory` |

## See Also

- **[Type Annotations](type-annotations.md)** - Detailed type system guide
- **[Basic Usage](../getting-started/basic-usage.md)** - Core concepts and patterns
- **[Troubleshooting](../guides/troubleshooting.md)** - Common issues and solutions
- **[Module CLI Guide](../module-cli-guide.md)** - Function-based CLI guide
- **[Class CLI Guide](../class-cli-guide.md)** - Method-based CLI guide

---

**Navigation**: [← Help Hub](../help.md) | [Type Annotations →](type-annotations.md)  
**Examples**: [Module Example](../../mod_example.py) | [Class Example](../../cls_example.py)
# Type Annotations Reference

[← Back to Help](../help.md) | [🏗️ Basic Usage](../getting-started/basic-usage.md)

## Table of Contents
- [Overview](#overview)
- [Required vs Optional Types](#required-vs-optional-types)
- [Basic Types](#basic-types)
- [Collection Types](#collection-types)
- [Optional and Union Types](#optional-and-union-types)
- [Enum Types](#enum-types)
- [Advanced Types](#advanced-types)
- [Type Validation](#type-validation)
- [Custom Type Handlers](#custom-type-handlers)
- [Common Issues](#common-issues)
- [See Also](#see-also)

## Overview

Type annotations are **required** for all parameters in functions/methods that will be exposed as CLI commands. Auto-CLI-Py uses these annotations to:

- Generate appropriate command-line arguments
- Perform input validation
- Create helpful error messages
- Generate accurate help text

**Critical Rule**: Every parameter must have a type annotation, or the function will be rejected.

## Required vs Optional Types

### Required Parameters (No Default Value)

```python
def process_file(input_file: str, output_format: str) -> None:
    """Process a file with specified format."""
    pass

# CLI Usage: Both parameters are required
# python script.py process-file --input-file data.txt --output-format json
```

### Optional Parameters (With Default Values)

```python
def process_file(
    input_file: str,                    # Required
    output_format: str = "json",        # Optional with default
    verbose: bool = False              # Optional flag
) -> None:
    """Process a file with optional settings."""
    pass

# CLI Usage: Only input-file is required
# python script.py process-file --input-file data.txt
# python script.py process-file --input-file data.txt --output-format csv --verbose
```

## Basic Types

### String (`str`)

```python
def greet(name: str, message: str = "Hello") -> None:
    """Greet someone with a message."""
    print(f"{message}, {name}!")

# CLI: --name VALUE, --message VALUE
# Usage: --name "John" --message "Hi there"
```

**Behavior**:
- Accepts any text input
- Automatically handles quoted strings
- Empty strings are valid

### Integer (`int`)

```python
def repeat_action(count: int, max_attempts: int = 10) -> None:
    """Repeat an action a specified number of times."""
    for i in range(min(count, max_attempts)):
        print(f"Action {i+1}")

# CLI: --count INTEGER, --max-attempts INTEGER  
# Usage: --count 5 --max-attempts 3
```

**Behavior**:
- Validates input is a valid integer
- Negative numbers supported: `--count -5`
- Rejects floats: `--count 3.14` → Error

### Float (`float`)

```python
def calculate_interest(principal: float, rate: float = 0.05) -> None:
    """Calculate compound interest."""
    interest = principal * rate
    print(f"Interest: ${interest:.2f}")

# CLI: --principal FLOAT, --rate FLOAT
# Usage: --principal 1000.0 --rate 0.03
```

**Behavior**:
- Accepts integers and floats: `3`, `3.14`, `0.5`
- Scientific notation: `1e-5`, `2.5e3`
- Negative values supported

### Boolean (`bool`)

```python
def backup_files(source_dir: str, compress: bool = False, verify: bool = True) -> None:
    """Backup files with optional compression and verification."""
    print(f"Backing up {source_dir}")
    if compress:
        print("Using compression")
    if verify:
        print("Verification enabled")

# CLI: --source-dir TEXT, --compress (flag), --verify/--no-verify
# Usage: --source-dir /data --compress --no-verify
```

**Boolean Flag Behavior**:
- `compress: bool = False` → `--compress` flag (presence = True)
- `verify: bool = True` → `--verify/--no-verify` flags
- Default `False` → Single flag to enable
- Default `True` → Dual flags to enable/disable

## Collection Types

### List of Strings (`List[str]`)

```python
from typing import List

def process_files(files: List[str], extensions: List[str] = None) -> None:
    """Process multiple files with optional extension filtering."""
    if extensions is None:
        extensions = ['.txt', '.py']
    
    for file in files:
        print(f"Processing: {file}")

# CLI: --files FILE1 FILE2 FILE3, --extensions EXT1 EXT2
# Usage: --files data.txt log.txt config.py --extensions .txt .log
```

**List Behavior**:
- Multiple values: `--files file1.txt file2.txt file3.txt`
- Single value: `--files single_file.txt`
- Empty list handling via default values

### List of Integers (`List[int]`)

```python
from typing import List

def analyze_numbers(values: List[int], thresholds: List[int] = None) -> None:
    """Analyze a list of numbers against thresholds."""
    if thresholds is None:
        thresholds = [10, 50, 100]
    
    print(f"Values: {values}")
    print(f"Thresholds: {thresholds}")

# CLI: --values 1 2 3 4, --thresholds 5 25 75
# Usage: --values 12 45 78 23 --thresholds 20 60
```

## Optional and Union Types

### Optional Types (`Optional[T]`)

```python
from typing import Optional

def connect_database(
    host: str,
    database: str,
    username: Optional[str] = None,
    password: Optional[str] = None,
    port: Optional[int] = None
) -> None:
    """Connect to database with optional authentication."""
    print(f"Connecting to {host}")
    if username:
        print(f"Username: {username}")
    if port:
        print(f"Port: {port}")

# CLI: All parameters become optional if they have None default
# Usage: --host localhost --database mydb --username admin --port 5432
```

**Optional Type Behavior**:
- `Optional[str]` with default `None` → Optional string parameter
- Can be omitted entirely from command line
- `None` value passed to function when not provided

### Union Types (`Union[str, int]`)

```python
from typing import Union

def process_identifier(id_value: Union[str, int], format_output: bool = False) -> None:
    """Process an identifier that can be string or integer."""
    if isinstance(id_value, int):
        print(f"Processing numeric ID: {id_value}")
    else:
        print(f"Processing string ID: {id_value}")

# CLI: Auto-CLI-Py will try int first, then str
# Usage: --id-value 12345 or --id-value "user_abc123"
```

**Union Type Behavior**:
- Tries types in order: `Union[int, str]` tries int first
- First successful conversion is used
- Limited support - prefer specific types when possible

## Enum Types

Enums create choice parameters with validation:

```python
from enum import Enum

class LogLevel(Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"

class OutputFormat(Enum):
    JSON = "json"
    CSV = "csv"
    XML = "xml"

def process_logs(
    log_file: str,
    level: LogLevel = LogLevel.INFO,
    output_format: OutputFormat = OutputFormat.JSON
) -> None:
    """Process log files with specified level and output format."""
    print(f"Processing {log_file} at {level.value} level")
    print(f"Output format: {output_format.value}")

# CLI: --level {debug,info,warning,error}, --output-format {json,csv,xml}
# Usage: --log-file app.log --level debug --output-format csv
```

**Enum Behavior**:
- Creates choice parameters with validation
- Case-sensitive matching
- Help text shows available choices
- Invalid choices produce clear error messages

### String Enum Pattern

```python
class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium" 
    HIGH = "high"
    CRITICAL = "critical"

def create_task(title: str, priority: Priority = Priority.MEDIUM) -> None:
    """Create a task with specified priority."""
    print(f"Task: {title} (Priority: {priority.value})")

# CLI validates against enum values
# Usage: --title "Fix bug" --priority high
```

### Integer Enum Pattern

```python
class CompressionLevel(Enum):
    NONE = 0
    LOW = 1
    MEDIUM = 5
    HIGH = 9

def compress_file(file_path: str, level: CompressionLevel = CompressionLevel.MEDIUM) -> None:
    """Compress file with specified compression level."""
    print(f"Compressing {file_path} at level {level.value}")
```

## Advanced Types

### Path-like Types

```python
from pathlib import Path

def process_directory(input_dir: Path, output_dir: Path = Path("./output")) -> None:
    """Process files in directory using Path objects."""
    print(f"Input: {input_dir}")
    print(f"Output: {output_dir}")
    
    # Path objects have useful methods
    if input_dir.exists():
        print("Input directory exists")

# CLI: Accepts string paths, converts to Path objects
# Usage: --input-dir /data/source --output-dir /data/processed
```

### Complex Default Handling

```python
from typing import List, Dict, Optional
import json

def configure_app(
    config_file: str,
    overrides: Optional[List[str]] = None,
    debug: bool = False
) -> None:
    """Configure application with optional parameter overrides."""
    if overrides is None:
        overrides = []
    
    print(f"Loading config from: {config_file}")
    print(f"Overrides: {overrides}")

# Safe handling of mutable defaults
# Usage: --config-file app.json --overrides "key1=value1" "key2=value2" --debug
```

## Type Validation

### Built-in Validation

Auto-CLI-Py automatically validates input based on type annotations:

```python
def calculate_stats(numbers: List[int], precision: int = 2) -> None:
    """Calculate statistics with input validation."""
    pass

# Automatic validation:
# --numbers abc def → Error: invalid int value
# --numbers 1 2 3 → Success: [1, 2, 3]
# --precision 3.14 → Error: invalid int value
# --precision 4 → Success: 4
```

### Error Messages

Clear error messages for type mismatches:

```bash
$ python script.py calculate-stats --numbers 1 abc 3
Error: Invalid value 'abc' for '--numbers': invalid literal for int()

$ python script.py calculate-stats --numbers 1 2 3 --precision 3.5
Error: Invalid value '3.5' for '--precision': invalid literal for int()
```

## Custom Type Handlers

For advanced use cases, you can handle complex types:

```python
import json
from typing import Dict, Any

def process_config(
    settings: str,  # JSON string that we'll parse manually
    validate: bool = True
) -> None:
    """Process configuration from JSON string."""
    try:
        config_dict = json.loads(settings)
        print(f"Config: {config_dict}")
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")

# Usage: --settings '{"key": "value", "debug": true}'
```

### File Content Processing

```python
def process_data_file(data_file: str, encoding: str = "utf-8") -> None:
    """Process data from file (pass filename, not content)."""
    try:
        with open(data_file, 'r', encoding=encoding) as f:
            content = f.read()
        print(f"Loaded {len(content)} characters")
    except FileNotFoundError:
        print(f"File not found: {data_file}")

# CLI handles file path, function handles file operations
# Usage: --data-file data.txt --encoding utf-8
```

## Common Issues

### 1. Missing Import Statements

```python
# ❌ Error: List not imported
def process_items(items: List[str]) -> None:
    pass

# ✅ Fix: Import required types
from typing import List

def process_items(items: List[str]) -> None:
    pass
```

### 2. Type Annotation Syntax Errors

```python
# ❌ Error: Invalid syntax
def bad_function(count: int = str) -> None:  # Type as default
    pass

# ✅ Fix: Proper annotation
def good_function(count: int = 5) -> None:
    pass
```

### 3. Mutable Default Arguments

```python
# ❌ Dangerous: Mutable default
def bad_function(items: List[str] = []) -> None:
    items.append("new_item")  # Modifies shared default!

# ✅ Safe: None default with initialization
def good_function(items: List[str] = None) -> None:
    if items is None:
        items = []
    items.append("new_item")
```

### 4. Complex Types Not Supported

```python
# ❌ Too complex for direct CLI mapping
def complex_function(callback: Callable[[str], int]) -> None:
    pass

# ✅ Use simpler types and handle complexity internally
def simple_function(function_name: str) -> None:
    """Use function name to look up actual callable."""
    callbacks = {
        'process': process_callback,
        'validate': validate_callback
    }
    callback = callbacks.get(function_name)
    if callback:
        result = callback("test")
```

### 5. Return Type Annotations

```python
# ✅ Good: Include return type (recommended)
def process_data(data: str) -> None:
    print(f"Processing: {data}")

# ⚠️ Works but not recommended: Missing return type  
def process_data(data: str):
    print(f"Processing: {data}")
```

## Best Practices

### 1. Use Specific Types

```python
# ✅ Preferred: Specific types
def configure_server(host: str, port: int, ssl_enabled: bool = False) -> None:
    pass

# ❌ Less ideal: Generic types
def configure_server(host: str, port: str, ssl_enabled: str = "false") -> None:
    # Requires manual validation and conversion
    pass
```

### 2. Provide Sensible Defaults

```python
# ✅ Good: Useful defaults
def backup_database(
    database_name: str,
    backup_dir: str = "./backups",
    compress: bool = True,
    max_age_days: int = 30
) -> None:
    pass
```

### 3. Use Enums for Choices

```python
# ✅ Preferred: Enum for limited choices
class Format(Enum):
    JSON = "json"
    CSV = "csv"
    XML = "xml"

def export_data(data: str, format: Format = Format.JSON) -> None:
    pass

# ❌ Less robust: String with manual validation
def export_data(data: str, format: str = "json") -> None:
    if format not in ["json", "csv", "xml"]:
        raise ValueError(f"Invalid format: {format}")
```

## See Also

- **[Basic Usage](../getting-started/basic-usage.md)** - Core concepts and patterns
- **[Module CLI Guide](../module-cli-guide.md)** - Function-based CLI details
- **[Class CLI Guide](../class-cli-guide.md)** - Method-based CLI details
- **[API Reference](../reference/api.md)** - Complete method reference
- **[Troubleshooting](../guides/troubleshooting.md)** - Common issues and solutions

---

**Navigation**: [← Help Hub](../help.md) | [Basic Usage →](../getting-started/basic-usage.md)  
**Examples**: [Module Example](../../mod_example.py) | [Class Example](../../cls_example.py)
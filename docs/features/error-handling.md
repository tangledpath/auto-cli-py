# Error Handling

[← Back to Features](index.md) | [↑ Documentation Hub](../help.md)

## Overview

Auto-CLI-Py provides comprehensive error handling to ensure user-friendly error messages and proper exit codes.

## Error Types

### Type Validation Errors
When arguments don't match expected types:
```bash
$ my-cli process --count "not-a-number"
Error: Invalid value for --count: 'not-a-number' is not a valid integer
```

### Missing Required Arguments
```bash
$ my-cli process
Error: Missing required argument: input_file
```

### Invalid Enum Values
```bash
$ my-cli process --format INVALID
Error: Invalid choice for --format: 'INVALID'
Valid choices are: json, csv, xml
```

## Handling Errors in Your Code

### Return Exit Codes
```python
def process_file(file_path: str) -> None:
    """Process a file with proper error handling."""
    if not Path(file_path).exists():
        print(f"Error: File not found: {file_path}")
        return 1  # Return non-zero for error
    
    try:
        # Process file
        print(f"Processing {file_path}")
        return 0  # Success
    except Exception as e:
        print(f"Error processing file: {e}")
        return 2  # Different error code
```

### Validation in Methods
```python
class DataProcessor:
    def analyze(self, threshold: float) -> None:
        """Analyze data with validation."""
        if not 0 <= threshold <= 1:
            print("Error: Threshold must be between 0 and 1")
            return 1
        
        # Continue processing
```

### Using Exceptions
```python
class APIClient:
    def connect(self, url: str) -> None:
        """Connect to API with exception handling."""
        try:
            # Connection logic
            if not url.startswith(('http://', 'https://')):
                raise ValueError("URL must start with http:// or https://")
        except ValueError as e:
            print(f"Error: {e}")
            return 1
        except Exception as e:
            print(f"Unexpected error: {e}")
            return 2
```

## Best Practices

### Clear Error Messages
```python
# ❌ Poor error message
print("Error!")

# ✅ Clear, actionable message
print(f"Error: Cannot read file '{filename}'. Please check the file exists and you have read permissions.")
```

### Consistent Exit Codes
```python
# Common exit code conventions
SUCCESS = 0
GENERAL_ERROR = 1
MISUSE_ERROR = 2
CANNOT_EXECUTE = 126
COMMAND_NOT_FOUND = 127
```

### Error Message Format
```python
def format_error(message: str, suggestion: str = None) -> str:
    """Format error messages consistently."""
    output = f"❌ Error: {message}"
    if suggestion:
        output += f"\n💡 Suggestion: {suggestion}"
    return output
```

## Debugging

### Enable Debug Mode
```python
class DebugCLI:
    def __init__(self, debug: bool = False):
        self.debug = debug
    
    def process(self, file: str) -> None:
        try:
            # Processing logic
            pass
        except Exception as e:
            if self.debug:
                import traceback
                traceback.print_exc()
            else:
                print(f"Error: {e}")
```

### Verbose Error Output
```bash
# Set environment variable for debugging
export AUTO_CLI_DEBUG=1
python my_cli.py command --args
```

## User-Friendly Features

### Suggestions for Typos
Auto-CLI-Py can suggest correct commands for typos:
```bash
$ my-cli porcess
Error: Unknown command 'porcess'
Did you mean 'process'?
```

### Help on Error
Show help when commands fail:
```bash
$ my-cli process
Error: Missing required argument: input_file

Usage: my-cli process --input-file FILE [OPTIONS]

Run 'my-cli process --help' for more information.
```

## See Also

- [Type Annotations](type-annotations.md) - Type validation
- [Troubleshooting](../guides/troubleshooting.md) - Common errors
- [Best Practices](../guides/best-practices.md) - Error handling patterns

---

**Navigation**: [← Shell Completion](shell-completion.md) | [Features Index →](index.md)
# Troubleshooting Guide

[← Back to Guides](index.md) | [↑ Documentation Hub](../help.md)

## Common Issues and Solutions

### Installation Issues

#### Problem: "No module named 'auto_cli'"
**Solution**: Install the package correctly
```bash
pip install auto-cli-py  # Note: package name has dashes
```

#### Problem: "auto_cli module not found" after installation
**Solution**: Check your Python environment
```bash
# Verify installation
pip show auto-cli-py

# If using virtual environment, ensure it's activated
which python
which pip
```

### Type Annotation Issues

#### Problem: "Function parameters must have type annotations"
**Solution**: Add type hints to all parameters
```python
# ❌ Wrong
def process(input_file, output_dir, verbose=False):
    pass

# ✅ Correct
def process(input_file: str, output_dir: str, verbose: bool = False) -> None:
    pass
```

#### Problem: "Unsupported type annotation"
**Solution**: Use supported types
```python
# ❌ Complex types not supported
def analyze(callback: Callable[[str], int]) -> None:
    pass

# ✅ Use simpler alternatives
def analyze(callback_name: str) -> None:
    pass
```

### Class-based CLI Issues

#### Problem: "Constructor parameters must have default values"
**Solution**: Add defaults to all constructor parameters
```python
# ❌ Wrong
class MyCLI:
    def __init__(self, config_file):
        self.config_file = config_file

# ✅ Correct
class MyCLI:
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
```

#### Problem: "Inner class constructor needs defaults"
**Solution**: Add defaults to inner class constructors too
```python
class MyCLI:
    def __init__(self, debug: bool = False):
        self.debug = debug
    
    class GroupCommands:
        # ❌ Wrong
        def __init__(self, database_url):
            pass
        
        # ✅ Correct
        def __init__(self, database_url: str = "sqlite:///app.db"):
            self.database_url = database_url
```

### Runtime Issues

#### Problem: "Command not found"
**Solution**: Check function/method naming
- Functions starting with `_` are ignored
- Method names are converted to kebab-case
- Use `--help` to see available commands

#### Problem: "Unexpected argument error"
**Solution**: Check parameter names
```bash
# Parameter names use dashes, not underscores
python cli.py command --input-file data.txt  # Correct
python cli.py command --input_file data.txt  # Wrong
```

### Output and Display Issues

#### Problem: "No colors in output"
**Solution**: Check color settings
```python
# Force enable colors
cli = CLI(MyClass, no_color=False)

# Or check NO_COLOR environment variable
unset NO_COLOR
```

#### Problem: "Help text not showing"
**Solution**: Add docstrings
```python
def process_data(input_file: str) -> None:
    """Process data from input file.
    
    This function reads and processes the specified file.
    
    Args:
        input_file: Path to the input data file
    """
    pass
```

### Performance Issues

#### Problem: "Slow CLI startup"
**Solution**: Optimize imports
```python
# Move heavy imports inside functions
def process_data(file: str) -> None:
    import pandas as pd  # Import only when needed
    # Process with pandas
```

### Testing Issues

#### Problem: "CLI tests failing"
**Solution**: Test functions directly
```python
# Test the function, not the CLI
def test_process():
    result = process_data("test.txt")
    assert result == expected_value
```

## Debug Mode

Enable debug output for more information:
```bash
# Set debug environment variable
export AUTO_CLI_DEBUG=1
python my_cli.py --help
```

## Getting Help

If you're still having issues:

1. Check the [FAQ](../faq.md)
2. Search [GitHub Issues](https://github.com/tangledpath/auto-cli-py/issues)
3. Ask in [Discussions](https://github.com/tangledpath/auto-cli-py/discussions)
4. File a [bug report](https://github.com/tangledpath/auto-cli-py/issues/new)

---

**Navigation**: [← Guides](index.md) | [Best Practices →](best-practices.md)
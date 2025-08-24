# Guides

[↑ Documentation Hub](../help.md)

Practical guides and how-to documentation for common tasks.

## Available Guides

### 🔧 [Troubleshooting](troubleshooting.md)
Solutions to common problems and issues.
- Installation problems
- Import errors
- Type annotation issues
- Runtime errors
- Performance problems

### 📚 [Best Practices](best-practices.md)
Recommended patterns and conventions.
- Code organization
- Naming conventions
- Documentation standards
- Testing strategies
- Performance tips

### 💡 [Examples](examples.md)
Real-world CLI examples and use cases.
- File processing tools
- Database management CLIs
- API client tools
- DevOps utilities
- Data analysis scripts

## Quick Solutions

### Common Issues

**Problem**: "No module named 'auto_cli'"
```bash
# Solution: Install the package
pip install auto-cli-py
```

**Problem**: "Function missing type annotations"
```python
# Before (won't work)
def process(file, count):
    pass

# After (correct)
def process(file: str, count: int) -> None:
    pass
```

**Problem**: "Constructor parameters need defaults"
```python
# Before (won't work)
class MyCLI:
    def __init__(self, config_file):
        pass

# After (correct)
class MyCLI:
    def __init__(self, config_file: str = "config.json"):
        pass
```

### Best Practice Examples

**Clear Function Names**
```python
# Good
def compress_file(input_path: str, output_path: str = None) -> None:
    """Compress a file to the specified output."""
    pass

# Avoid
def proc(i: str, o: str = None) -> None:
    """Process."""
    pass
```

**Comprehensive Docstrings**
```python
def analyze_logs(
    log_file: str,
    pattern: str,
    output_format: str = "json"
) -> None:
    """
    Analyze log files for specific patterns.
    
    Searches through log files and extracts entries matching
    the given pattern, formatting results as requested.
    
    Args:
        log_file: Path to the log file to analyze
        pattern: Regular expression pattern to match
        output_format: Output format (json, csv, or table)
        
    Example:
        analyze_logs("app.log", "ERROR.*timeout", "csv")
    """
    pass
```

## How-To Recipes

### Create a Multi-Command CLI
See [Module CLI Guide](../user-guide/module-cli.md#hierarchical-commands) for hierarchical commands.

### Add Custom Validation
See [Advanced Configuration](../advanced/custom-configuration.md#validation-hooks) for validation patterns.

### Enable Shell Completion
See [Shell Completion](../features/shell-completion.md) for setup instructions.

### Test Your CLI
See [Testing CLIs](../advanced/testing-clis.md) for comprehensive testing strategies.

## Community Guides

Have a guide to share? We welcome contributions! See our [Contributing Guide](../development/contributing.md).

## Next Steps

- Solve problems with [Troubleshooting](troubleshooting.md)
- Learn [Best Practices](best-practices.md)
- Explore [Examples](examples.md)
- Check the [FAQ](../faq.md)

---

**Still stuck?** Open an issue on [GitHub](https://github.com/tangledpath/auto-cli-py/issues)
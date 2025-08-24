# User Guide

[↑ Documentation Hub](../help.md)

Comprehensive documentation for Auto-CLI-Py users. This guide covers all aspects of creating and managing CLIs.

## Core Concepts

### 🗂️ [Module CLI Guide](module-cli.md)
Complete guide to creating CLIs from Python functions.
- Function design and requirements
- Hierarchical command organization
- Advanced module patterns
- Testing and best practices

### 🏗️ [Class CLI Guide](class-cli.md)
Complete guide to creating CLIs from Python classes.
- Class design patterns
- State management techniques
- Method organization
- Constructor requirements

### 🏢 [Inner Classes Pattern](inner-classes.md)
Using inner classes for organized command structure.
- Flat commands with double-dash notation
- Global and sub-global arguments
- Command organization strategies
- Real-world examples

### 🔄 [Mode Comparison](mode-comparison.md)
Detailed comparison of module vs class approaches.
- Feature-by-feature analysis
- Use case recommendations
- Migration strategies
- Performance considerations

## Key Topics Covered

### Module CLI Features
- Creating commands from functions
- Type annotation requirements
- Parameter handling and defaults
- Function filtering and organization
- Command hierarchies with double underscores

### Class CLI Features
- Creating commands from methods
- Instance lifecycle management
- State persistence between commands
- Constructor parameter handling
- Method visibility control

### Common Patterns
- Error handling strategies
- Configuration management
- Resource handling
- Testing approaches
- Documentation best practices

## Quick Examples

### Module CLI
```python
from auto_cli import CLI
import sys

def process_data(input_file: str, format: str = "json") -> None:
    """Process data file."""
    print(f"Processing {input_file} as {format}")

if __name__ == '__main__':
    cli = CLI(sys.modules[__name__])
    cli.display()
```

### Class CLI
```python
from auto_cli import CLI

class DataProcessor:
    """Data processing application."""
    
    def __init__(self, default_format: str = "json"):
        self.default_format = default_format
    
    def process(self, file: str) -> None:
        """Process a file."""
        print(f"Processing {file} as {self.default_format}")

if __name__ == '__main__':
    cli = CLI(DataProcessor)
    cli.display()
```

## Next Steps

- Explore [Features](../features/index.md) for advanced capabilities
- Check [Advanced Topics](../advanced/index.md) for complex scenarios
- See [Examples](../guides/examples.md) for real-world applications

---

**Need help?** Check the [Troubleshooting Guide](../guides/troubleshooting.md) or [FAQ](../faq.md)
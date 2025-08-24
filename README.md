# auto-cli-py

## Table of Contents
- [Documentation](#documentation)
- [Quick Start](#quick-start)
- [Two CLI Creation Modes](#two-cli-creation-modes)
- [Development](#development)

Python Library that builds complete CLI applications from your existing code using introspection and type annotations. Supports **module-based** and **class-based** CLI creation with **flat command architecture**.

Most options are set using introspection/signature and annotation functionality, so very little configuration has to be done. The library analyzes your function signatures and automatically creates command-line interfaces with proper argument parsing, type checking, and help text generation.

**🆕 ARCHITECTURE UPDATE**: All CLIs now use **flat commands** - no hierarchical command groups. Inner class methods become flat commands with double-dash notation (e.g., `data-operations--process`).

## 📚 Documentation
**[→ Complete Documentation Hub](docs/help.md)** - Comprehensive guides and examples

## Quick Start
**[→ Quick Start](docs/quick-start.md#installation)** - Comprehensive guides and examples

### Quick Links
- **[Module-based CLI Guide](docs/module-cli-guide.md)** - Create CLIs from module functions  
- **[Class-based CLI Guide](docs/class-cli-guide.md)** - Create CLIs from class methods
- **[Getting Started](docs/getting-started/quick-start.md)** - 5-minute introduction

## Two CLI Creation Modes

### 🗂️ Module-based CLI (Flat Commands Only)
Perfect for functional programming styles and simple utilities. All functions become flat commands:

```python
# Create CLI from module functions
from auto_cli import CLI
import sys

def greet(name: str = "World", excited: bool = False) -> None:
    """Greet someone by name."""
    greeting = f"Hello, {name}!"
    if excited:
        greeting += " 🎉"
    print(greeting)

if __name__ == '__main__':
    cli = CLI(sys.modules[__name__], title="My CLI")
    cli.display()
```

### 🏗️ Class-based CLI (Flat with Double-Dash Notation)
Ideal for stateful applications and object-oriented designs. Supports both **direct methods** (simple) and **inner class patterns** (flat with organized naming):

#### Direct Methods (Simple Commands)
```python
from auto_cli import CLI

class Calculator:
    """Simple calculator."""
    
    def __init__(self):
        pass
    
    def add(self, a: float, b: float) -> None:
        """Add two numbers."""
        print(f"{a} + {b} = {a + b}")

if __name__ == '__main__':
    cli = CLI(Calculator)
    cli.display()

# Usage: python calc.py add --a 5 --b 3
```

#### Inner Classes (Flat Commands with Double-Dash Notation)

```python
# Inner Class Pattern (NEW) - Flat commands with organized naming
from auto_cli import CLI

class UserManager:
    """User management with flat double-dash commands."""
    
    def __init__(self, config_file: str = "config.json"):  # Global arguments
        self.config_file = config_file
    
    class UserOperations:
        """User account operations."""
        
        def __init__(self, database_url: str = "sqlite:///users.db"):  # Sub-global arguments  
            self.database_url = database_url
        
        def create(self, username: str, email: str, active: bool = True) -> None:  # Command arguments
            """Create a new user account."""
            print(f"Creating user: {username}")

if __name__ == '__main__':
    cli = CLI(UserManager)  
    cli.display()

# Usage: python app.py --config-file prod.json user-operations--create --database-url postgres://... --username alice --email alice@test.com
```

### Choose Your Approach

All approaches automatically generate CLIs with:
- Proper argument parsing from type annotations
- Help text generation from docstrings  
- Type checking and validation
- Built-in themes and customization options
- **FLAT COMMANDS**: All commands are flat - no hierarchical groups
- **DOUBLE-DASH NOTATION**: Inner class methods use `class-name--method-name` format

**📋 Class-based CLI Requirements**: All constructor parameters (main class and inner classes) must have default values.

**See [Complete Documentation](docs/help.md) for detailed guides and examples.**

## Development

This project uses Poetry for dependency management and modern Python tooling.

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/tangledpath/auto-cli-py.git
cd auto-cli-py

# Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# Setup development environment
./bin/setup-dev.sh
```

### Development Commands

```bash
# Install dependencies
poetry install

# Run tests
./bin/test.sh
# Or directly: poetry run pytest

# Run linting and formatting
./bin/lint.sh

# Run examples
poetry run python mod_example.py  # Module-based CLI
poetry run python cls_example.py  # Class-based CLI

# Build package
poetry build

# Publish to PyPI (maintainers only)
./bin/publish.sh
```

### Code Quality

The project uses several tools for code quality:
- **Black**: Code formatting
- **Ruff**: Fast Python linter
- **MyPy**: Type checking  
- **Pylint**: Additional linting
- **Pre-commit**: Automated checks on commit

### Testing

```bash
# Run all tests with coverage
poetry run pytest

# Run specific test file
poetry run pytest tests/test_cli.py

# Run with verbose output
poetry run pytest -v
```

### Requirements

- Python 3.13.5+
- No runtime dependencies (uses only standard library)

# Auto-CLI-Py Documentation

[← Back to README](../README.md) | [⚙️ Development Guide](../CLAUDE.md)

## Documentation Structure

### 📚 Core Documentation
- **[Getting Started](getting-started/index.md)** - Installation, quick start, and basics
- **[User Guide](user-guide/index.md)** - Comprehensive guides for both CLI modes
- **[Features](features/index.md)** - Type annotations, themes, completion, and more
- **[Advanced Topics](advanced/index.md)** - State management, testing, migration
- **[API Reference](reference/index.md)** - Complete API documentation

### 🛠️ Resources
- **[Guides](guides/index.md)** - Troubleshooting, best practices, examples
- **[FAQ](faq.md)** - Frequently asked questions
- **[Development](development/index.md)** - For contributors and maintainers

## Table of Contents
- [Overview](#overview)
- [Two CLI Creation Modes](#two-cli-creation-modes)
- [Quick Comparison](#quick-comparison)
- [Getting Started](#getting-started)
- [Feature Highlights](#feature-highlights)
- [Next Steps](#next-steps)

## Overview

Auto-CLI-Py is a Python library that automatically builds complete CLI applications from your existing code using introspection and type annotations. It supports two distinct modes of operation, each designed for different use cases and coding styles.

## Two CLI Creation Modes

### 🗂️ Module-based CLI
Create CLIs from module functions - perfect for functional programming styles and simple utilities.

```python
# mod_example.py
def greet(name: str, excited: bool = False) -> None:
    """Greet someone by name."""
    greeting = f"Hello, {name}!"
    if excited:
        greeting += " 🎉"
    print(greeting)

# Create CLI from module
from auto_cli import CLI
import sys
cli = CLI.from_module(sys.modules[__name__], title="My Module CLI")
cli.display()
```

### 🏗️ Class-based CLI
Create CLIs from class methods - ideal for stateful applications and object-oriented designs. Supports two patterns:

#### **🆕 Inner Class Pattern (Recommended)**
Use inner classes for hierarchical command organization with three argument levels:

```python
# cls_example.py
class UserManager:
    """User management CLI with hierarchical commands."""
    
    def __init__(self, config_file: str = "config.json", debug: bool = False):
        """Initialize with global arguments.
        
        :param config_file: Configuration file (global argument)
        :param debug: Enable debug mode (global argument)
        """
        self.config_file = config_file
        self.debug = debug
    
    class UserOperations:
        """User account operations."""
        
        def __init__(self, database_url: str = "sqlite:///users.db"):
            """Initialize user operations.
            
            :param database_url: Database connection URL (sub-global argument)
            """
            self.database_url = database_url
        
        def create(self, username: str, email: str, active: bool = True) -> None:
            """Create a new user account.
            
            :param username: Username for new account
            :param email: Email address
            :param active: Whether account is active
            """
            print(f"Creating user {username} with {email}")
            print(f"Database: {self.database_url}")
    
    class ReportGeneration:
        """User reporting without sub-global arguments."""
        
        def summary(self, include_inactive: bool = False) -> None:
            """Generate user summary report."""
            print(f"Generating summary (inactive: {include_inactive})")

# Usage with three argument levels
# python user_mgr.py --config-file prod.json --debug \
#   user-operations --database-url postgresql://... \
#   create --username alice --email alice@example.com
```

#### **Traditional Pattern (Backward Compatible)**
Use dunder notation for existing applications:

```python
class UserManager:
    """Traditional dunder-based CLI pattern."""
    
    def add_user(self, username: str, email: str, active: bool = True) -> None:
        """Add a new user to the system."""
        user = {"username": username, "email": email, "active": active}
        self.users.append(user)
        print(f"Added user: {username}")
    
    def list_users(self, active_only: bool = False) -> None:
        """List all users in the system."""
        users_to_show = self.users
        if active_only:
            users_to_show = [u for u in users_to_show if u["active"]]
        
        for user in users_to_show:
            status = "✓" if user["active"] else "✗"
            print(f"{status} {user['username']} ({user['email']})")

# Create CLI from class
from auto_cli import CLI
cli = CLI.from_class(UserManager, theme_name="colorful")
cli.display()
```

## Quick Comparison

| Feature | Module-based | Class-based |
|---------|-------------|-------------|
| **Use Case** | Functional utilities, scripts | Stateful apps, complex workflows |
| **State Management** | Function parameters only | Instance variables + parameters |
| **Organization** | Functions in module | Methods in class |
| **CLI Creation** | `CLI.from_module(module)` | `CLI.from_class(SomeClass)` |
| **Title Source** | Manual or module docstring | Class docstring |
| **Best For** | Simple tools, data processing | Applications with persistent state |

## Getting Started

### 📚 New to Auto-CLI-Py?
- **[Quick Start Guide](getting-started/quick-start.md)** - Get running in 5 minutes
- **[Installation Guide](getting-started/installation.md)** - Detailed setup instructions
- **[Basic Usage Patterns](getting-started/basic-usage.md)** - Core concepts and examples
- **[Choosing CLI Mode](getting-started/choosing-cli-mode.md)** - Module vs Class decision guide

## Feature Guides

Both CLI modes support the same advanced features:

- **Type-driven interface generation** - Automatic CLI from type annotations
- **Zero configuration** - Works out of the box with sensible defaults
- **Beautiful help text** - Auto-generated from docstrings
- **Shell completion** - Tab completion for all shells
- **Colored output** - With theme support and NO_COLOR compliance

## Next Steps

### 🚀 For New Users
1. Start with **[Installation](getting-started/installation.md)**
2. Follow the **[Quick Start](getting-started/quick-start.md)**
3. Choose your mode: **[Module vs Class](getting-started/choosing-cli-mode.md)**
4. Read the appropriate guide: **[Module CLI](user-guide/module-cli.md)** or **[Class CLI](user-guide/class-cli.md)**

### 📖 For Learning
- **[User Guide](user-guide/index.md)** - Comprehensive documentation
- **[Features](features/index.md)** - Explore all capabilities
- **[Examples](guides/examples.md)** - Real-world use cases
- **[FAQ](faq.md)** - Common questions answered

### 🔧 For Advanced Users
- **[Advanced Topics](advanced/index.md)** - Complex patterns and techniques
- **[API Reference](reference/index.md)** - Complete API documentation
- **[Troubleshooting](guides/troubleshooting.md)** - Solve common problems
- **[Contributing](development/contributing.md)** - Help improve Auto-CLI-Py

---

**Navigation**: [README](../README.md) | [Development](../CLAUDE.md)
**Examples**: [Module Example](../mod_example.py) | [Class Example](../cls_example.py)
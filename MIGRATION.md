# Migration Guide: Hierarchical to Flat Command Architecture

This guide helps you migrate from auto-cli-py's old hierarchical command structure to the new flat command architecture.

## Overview of Changes

**OLD (Hierarchical)**: Commands were organized in groups like `python app.py user create --name alice`
**NEW (Flat)**: All commands are flat with double-dash notation like `python app.py user--create --name alice`

## What Changed

### 1. All Commands Are Now Flat

- **Module-based CLIs**: Functions become direct commands (no command group grouping)
- **Class-based CLIs**: All methods become flat commands using double-dash notation
- **No More Command Groups**: No hierarchical structures like `app.py group command`

### 2. Double-Dash Notation for Inner Classes

Inner class methods now use the format: `class-name--method-name`

### 3. Removed Dunder Notation Support

Method names like `user__create` are no longer supported for creating command groups.

## Migration Steps

### Step 1: Update Module-Based CLIs

**OLD (with dunder notation for command groups):**
```python
def user__create(name: str, email: str) -> None:
    """Create a user."""
    pass

def user__list() -> None:
    """List users."""
    pass

# Commands: user create, user list
```

**NEW (flat commands only):**
```python
def create_user(name: str, email: str) -> None:
    """Create a user."""
    pass

def list_users() -> None:
    """List users."""
    pass

# Commands: create-user, list-users
```

### Step 2: Update Class-Based CLIs

**OLD (hierarchical commands):**
```python
class UserManager:
    def __init__(self):
        pass
    
    def user__create(self, name: str, email: str) -> None:
        """Create user."""
        pass
    
    def user__delete(self, user_id: str) -> None:
        """Delete user."""
        pass

# Usage: python app.py user create --name alice
# Usage: python app.py user delete --user-id 123
```

**NEW (flat commands with double-dash):**
```python
class UserManager:
    def __init__(self):
        pass
    
    class UserOperations:
        def __init__(self):
            pass
        
        def create(self, name: str, email: str) -> None:
            """Create user."""
            pass
        
        def delete(self, user_id: str) -> None:
            """Delete user."""
            pass

# Usage: python app.py user-operations--create --name alice
# Usage: python app.py user-operations--delete --user-id 123
```

### Step 3: Update CLI Instantiation

**OLD (with deprecated parameters):**
```python
cli = CLI(MyClass, theme_tuner=True, completion=True)
```

**NEW (using System class for utilities):**
```python
from auto_cli.system import System

# For built-in utilities (theme tuning, completion)
cli = CLI(System, enable_completion=True)

# For your application
cli = CLI(MyClass, enable_completion=True)
```

### Step 4: Update Help Command Expectations

**OLD (hierarchical help):**
```bash
python app.py --help          # Shows command groups
python app.py user --help     # Shows user command groups  
python app.py user create --help  # Shows create command help
```

**NEW (flat help):**
```bash
python app.py --help                    # Shows all flat commands
python app.py user-operations--create --help  # Shows create command help
```

## Common Migration Patterns

### Pattern 1: Simple Command Renaming

**OLD:**
```python
def data__process(file: str) -> None:
    pass

def data__validate(file: str) -> None:
    pass
```

**NEW:**
```python
def process_data(file: str) -> None:
    pass

def validate_data(file: str) -> None:
    pass
```

### Pattern 2: Converting to Inner Classes

**OLD:**
```python
class AppCLI:
    def user__create(self, name: str) -> None:
        pass
    
    def user__delete(self, user_id: str) -> None:
        pass
    
    def config__set(self, key: str, value: str) -> None:
        pass
    
    def config__get(self, key: str) -> None:
        pass
```

**NEW:**
```python
class AppCLI:
    def __init__(self):
        pass
    
    class UserManagement:
        def __init__(self):
            pass
        
        def create(self, name: str) -> None:
            pass
        
        def delete(self, user_id: str) -> None:
            pass
    
    class Configuration:
        def __init__(self):
            pass
        
        def set(self, key: str, value: str) -> None:
            pass
        
        def get(self, key: str) -> None:
            pass
```

### Pattern 3: Global and Sub-Global Arguments

**OLD (not supported):**

**NEW (with inner class constructors):**
```python
class ProjectManager:
    def __init__(self, config_file: str = "config.json", debug: bool = False):
        """Global arguments available to all commands."""
        self.config_file = config_file
        self.debug = debug
    
    class DataOperations:
        def __init__(self, workspace: str = "./data", backup: bool = True):
            """Sub-global arguments for data operations."""
            self.workspace = workspace
            self.backup = backup
        
        def process(self, input_file: str, mode: str = "fast") -> None:
            """Command-specific arguments."""
            pass

# Usage: python app.py --config-file prod.json data-operations--process --workspace /tmp --backup --input-file data.txt --mode thorough
```

## Command Line Usage Changes

### Before (Hierarchical)
```bash
# User management
python app.py user create --name alice --email alice@test.com
python app.py user list --active-only
python app.py user delete --user-id 123

# Configuration
python app.py config set --key debug --value true
python app.py config get --key debug

# Help at different levels
python app.py --help           # Shows groups: user, config
python app.py user --help      # Shows: create, list, delete  
python app.py user create --help  # Shows create options
```

### After (Flat)
```bash
# User management (flat commands)
python app.py user-management--create --name alice --email alice@test.com
python app.py user-management--list --active-only
python app.py user-management--delete --user-id 123

# Configuration (flat commands)
python app.py configuration--set --key debug --value true
python app.py configuration--get --key debug

# Help (all commands shown in one list)
python app.py --help                           # Shows all flat commands
python app.py user-management--create --help   # Shows create options
```

## Built-in Utilities Migration

### Theme Tuning

**OLD:**
```python
cli = CLI(MyClass, theme_tuner=True)
```

**NEW:**
```python
from auto_cli.system import System

# Use System class for theme tuning
cli = CLI(System)
# Commands: tune-theme--increase-adjustment, tune-theme--toggle-theme, etc.
```

### Completion

**OLD:**
```python
cli = CLI(MyClass, completion=True)
```

**NEW:**
```python
from auto_cli.system import System

# Use System class for completion
cli = CLI(System, enable_completion=True)
# Commands: completion--install, completion--show
```

## Testing Your Migration

### 1. Update Test Commands
```python
# OLD test
result = subprocess.run(['python', 'app.py', 'user', 'create', '--name', 'test'])

# NEW test  
result = subprocess.run(['python', 'app.py', 'user-management--create', '--name', 'test'])
```

### 2. Verify Help Output
```bash
# Check that all expected flat commands appear
python app.py --help

# Verify individual command help
python app.py command-name--method-name --help
```

### 3. Update Documentation
- Update CLI usage examples in README files
- Update command examples in docstrings
- Update any shell scripts or automation that calls your CLI

## Troubleshooting

### Common Issues

**Issue**: `SystemExit: argument : invalid choice: 'user' (choose from user-management--create, ...)`
**Solution**: Update command usage from hierarchical (`user create`) to flat (`user-management--create`)

**Issue**: `AttributeError: 'CLI' object has no attribute 'theme_tuner'`
**Solution**: Remove deprecated parameters and use System class for built-in utilities

**Issue**: Commands not showing up
**Solution**: Ensure inner class constructors have default values for all parameters

### Migration Checklist

- [ ] Remove all dunder notation (`function__name`) from method names
- [ ] Convert to inner classes if organizing commands by groups
- [ ] Ensure all constructor parameters have default values
- [ ] Update CLI instantiation (remove `theme_tuner=True`, etc.)
- [ ] Update all command usage from hierarchical to flat format
- [ ] Update tests to use new flat command names
- [ ] Update documentation and examples
- [ ] Use System class for built-in utilities (theme tuning, completion)

## Need Help?

If you encounter issues during migration:

1. **Check the examples**: `cls_example.py` and `mod_example.py` show current patterns
2. **Run tests**: `poetry run pytest` to see working test patterns
3. **Review documentation**: See [docs/help.md](docs/help.md) for complete guides

The migration ensures a more consistent, predictable CLI interface while maintaining all the powerful features of auto-cli-py.
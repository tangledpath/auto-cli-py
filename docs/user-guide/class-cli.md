# Class-based CLI Guide

[← Back to Help](help.md) | [🗂️ Module-based Guide](module-cli-guide.md)

## Table of Contents
- [Overview](#overview)
- [When to Use Class-based CLI](#when-to-use-class-based-cli)
- [Basic Setup](#basic-setup)
- [Class Design Requirements](#class-design-requirements)
- [Complete Example Walkthrough](#complete-example-walkthrough)
- [State Management](#state-management)
- [Advanced Patterns](#advanced-patterns)
- [Best Practices](#best-practices)
- [See Also](#see-also)

## Overview

Class-based CLI creation allows you to build command-line interfaces from class methods, enabling stateful applications and object-oriented design patterns. The CLI automatically introspects your class methods and creates commands while maintaining an instance for state management.

**Perfect for**: Applications, configuration managers, stateful workflows, object-oriented designs, and complex interactive tools.

## When to Use Class-based CLI

Choose class-based CLI when you need:

✅ **Persistent state** - Data that persists between commands  
✅ **Complex workflows** - Multi-step operations with dependencies  
✅ **Object-oriented design** - Natural class hierarchies  
✅ **Configuration management** - Settings that affect multiple commands  
✅ **Resource management** - Database connections, file handles, etc.  
✅ **Interactive applications** - Tools with ongoing context  

❌ **Avoid when**:
- Simple, stateless operations are sufficient
- You prefer functional programming style
- Quick scripts that don't need complexity

## Basic Setup

### 1. Import and Create CLI

```python
from auto_cli import CLI

# At the end of your module
if __name__ == '__main__':
    cli = CLI.from_class(MyApplicationClass, theme_name="colorful")
    cli.display()
```

### 2. Factory Method Signature

```python
CLI.from_class(
    cls,                       # The class (not instance) to use
    title: str = None,         # CLI title (from class docstring if None)
    function_opts: dict = None,# Per-method options (optional)
    theme_name: str = 'universal', # Theme name
    no_color: bool = False,    # Disable colors
    completion: bool = True    # Enable shell completion
)
```

## Class Design Requirements

### Class Docstring (Recommended)

The CLI title is automatically extracted from your class docstring:

```python
class DatabaseManager:
    """
    Database Management CLI Tool
    
    A comprehensive tool for managing database operations,
    including backup, restore, and maintenance tasks.
    """
    
    def __init__(self):
        self.connection = None
        self.config = {}
```

### Method Requirements

Methods must follow the same requirements as module functions:

```python
class FileProcessor:
    """File processing application."""
    
    def __init__(self):
        self.processed_files = []
        self.config = {
            'default_format': 'json',
            'backup_enabled': True
        }
    
    def convert_file(
        self,
        input_file: str,
        output_format: str = "json",
        preserve_original: bool = True
    ) -> None:
        """
        Convert a single file to the specified format.
        
        Args:
            input_file: Path to the input file
            output_format: Target format (json, csv, xml)
            preserve_original: Keep the original file after conversion
        """
        # Access instance state
        if self.config['backup_enabled'] and preserve_original:
            print(f"Creating backup of {input_file}")
        
        print(f"Converting {input_file} to {output_format}")
        
        # Update instance state
        self.processed_files.append({
            'input': input_file,
            'format': output_format,
            'timestamp': datetime.now()
        })
```

### Private Methods

Methods starting with underscore are automatically excluded from CLI:

```python
class DataAnalyzer:
    """Data analysis tool."""
    
    def analyze_dataset(self, data_file: str) -> None:
        """Analyze the given dataset."""
        data = self._load_data(data_file)  # Private helper
        results = self._perform_analysis(data)  # Private helper
        self._save_results(results)  # Private helper
    
    def _load_data(self, file_path: str):
        """Private method - not exposed in CLI."""
        pass
    
    def _perform_analysis(self, data):
        """Private method - not exposed in CLI."""
        pass
    
    def _save_results(self, results):
        """Private method - not exposed in CLI."""
        pass
```

## Complete Example Walkthrough

Let's build a user management system using [cls_example.py](../cls_example.py):

### Step 1: Define Your Class

```python
# cls_example.py
"""User Management CLI Application"""

from enum import Enum
from typing import List, Optional
from datetime import datetime
import json

class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

class UserManager:
    """
    User Management System
    
    A comprehensive CLI tool for managing users, roles,
    and permissions in your application.
    """
    
    def __init__(self):
        self.users = []
        self.config = {
            'default_role': UserRole.USER,
            'require_email_verification': True,
            'max_users': 1000
        }
        self.session_stats = {
            'users_created': 0,
            'users_modified': 0,
            'commands_executed': 0
        }
    
    def add_user(
        self,
        username: str,
        email: str,
        role: UserRole = UserRole.USER,
        active: bool = True
    ) -> None:
        """
        Add a new user to the system.
        
        Creates a new user account with the specified details.
        The user will be added to the internal user database.
        
        Args:
            username: Unique username for the new user
            email: Email address for the user
            role: User role (admin, user, guest)
            active: Whether the user account is active
        """
        # Check for existing user
        if any(u['username'] == username for u in self.users):
            print(f"❌ Error: User '{username}' already exists")
            return
        
        # Validate email format (simple check)
        if '@' not in email:
            print(f"❌ Error: Invalid email format '{email}'")
            return
        
        # Create user
        user = {
            'username': username,
            'email': email,
            'role': role.value,
            'active': active,
            'created_at': datetime.now().isoformat(),
            'last_login': None
        }
        
        self.users.append(user)
        self.session_stats['users_created'] += 1
        
        print(f"✅ User '{username}' created successfully")
        print(f"   Email: {email}")
        print(f"   Role: {role.value}")
        print(f"   Active: {'Yes' if active else 'No'}")
    
    def list_users(
        self,
        role_filter: Optional[UserRole] = None,
        active_only: bool = False,
        format_output: str = "table"
    ) -> None:
        """
        List all users in the system.
        
        Display users with optional filtering by role and active status.
        
        Args:
            role_filter: Filter by specific role (optional)
            active_only: Show only active users
            format_output: Output format (table, json, csv)
        """
        users_to_show = self.users.copy()
        
        # Apply filters
        if role_filter:
            users_to_show = [u for u in users_to_show if u['role'] == role_filter.value]
        
        if active_only:
            users_to_show = [u for u in users_to_show if u['active']]
        
        if not users_to_show:
            print("No users found matching criteria")
            return
        
        # Format output
        if format_output == "json":
            print(json.dumps(users_to_show, indent=2))
        elif format_output == "csv":
            print("username,email,role,active,created_at")
            for user in users_to_show:
                print(f"{user['username']},{user['email']},{user['role']},{user['active']},{user['created_at']}")
        else:  # table format
            print(f"\\nFound {len(users_to_show)} users:")
            print("─" * 60)
            for user in users_to_show:
                status = "✅" if user['active'] else "❌"
                print(f"{status} {user['username']:<15} {user['email']:<25} ({user['role']})")
    
    def modify_user(
        self,
        username: str,
        new_email: Optional[str] = None,
        new_role: Optional[UserRole] = None,
        active: Optional[bool] = None
    ) -> None:
        """
        Modify an existing user's details.
        
        Update user information. Only provided parameters will be changed.
        
        Args:
            username: Username of user to modify
            new_email: New email address (optional)
            new_role: New role assignment (optional) 
            active: New active status (optional)
        """
        # Find user
        user = None
        for u in self.users:
            if u['username'] == username:
                user = u
                break
        
        if not user:
            print(f"❌ Error: User '{username}' not found")
            return
        
        # Track changes
        changes_made = []
        
        if new_email and new_email != user['email']:
            user['email'] = new_email
            changes_made.append(f"email → {new_email}")
        
        if new_role and new_role.value != user['role']:
            user['role'] = new_role.value
            changes_made.append(f"role → {new_role.value}")
        
        if active is not None and active != user['active']:
            user['active'] = active
            changes_made.append(f"active → {active}")
        
        if not changes_made:
            print(f"ℹ️  No changes made to user '{username}'")
            return
        
        self.session_stats['users_modified'] += 1
        
        print(f"✅ User '{username}' updated:")
        for change in changes_made:
            print(f"   {change}")
    
    def show_stats(self) -> None:
        """
        Display system statistics.
        
        Shows current system state including user counts,
        session statistics, and configuration.
        """
        total_users = len(self.users)
        active_users = sum(1 for u in self.users if u['active'])
        
        print("\\n📊 System Statistics")
        print("=" * 30)
        print(f"Total Users: {total_users}")
        print(f"Active Users: {active_users}")
        print(f"Inactive Users: {total_users - active_users}")
        
        # Role breakdown
        role_counts = {}
        for user in self.users:
            role = user['role']
            role_counts[role] = role_counts.get(role, 0) + 1
        
        print("\\n👥 Users by Role:")
        for role, count in role_counts.items():
            print(f"   {role}: {count}")
        
        # Session stats
        print("\\n🔄 Session Activity:")
        for key, value in self.session_stats.items():
            print(f"   {key.replace('_', ' ').title()}: {value}")
        
        # Configuration
        print("\\n⚙️  Configuration:")
        for key, value in self.config.items():
            if isinstance(value, Enum):
                value = value.value
            print(f"   {key.replace('_', ' ').title()}: {value}")
```

### Step 2: Create CLI

```python
# At the end of cls_example.py
if __name__ == '__main__':
    from auto_cli import CLI
    
    # Optional: Configure specific methods
    function_opts = {
        'add_user': {
            'description': 'Create a new user account'
        },
        'list_users': {
            'description': 'Display users with optional filtering'
        },
        'modify_user': {
            'description': 'Update existing user information'
        },
        'show_stats': {
            'description': 'Display system statistics and status'
        }
    }
    
    cli = CLI.from_class(
        UserManager,
        function_opts=function_opts,
        theme_name="colorful"
    )
    cli.display()
```

### Step 3: Usage Examples

```bash
# Run the CLI
python cls_example.py

# Create users
python cls_example.py add-user --username john --email john@example.com
python cls_example.py add-user --username admin --email admin@company.com --role ADMIN
python cls_example.py add-user --username guest --email guest@test.com --role GUEST --active False

# List users with filtering
python cls_example.py list-users
python cls_example.py list-users --role-filter ADMIN
python cls_example.py list-users --active-only --format-output json

# Modify users
python cls_example.py modify-user --username john --new-email john.doe@example.com
python cls_example.py modify-user --username guest --active True

# Show statistics
python cls_example.py show-stats
```

## State Management

### Instance Variables

The key advantage of class-based CLIs is persistent state between commands:

```python
class ProjectManager:
    """Project management CLI."""
    
    def __init__(self):
        self.current_project = None
        self.projects = {}
        self.global_config = {
            'auto_save': True,
            'backup_count': 3
        }
    
    def create_project(self, name: str, description: str = "") -> None:
        """Create a new project."""
        self.projects[name] = {
            'description': description,
            'tasks': [],
            'created_at': datetime.now()
        }
        self.current_project = name  # State persists!
        print(f"✅ Created project '{name}'")
    
    def add_task(self, title: str, priority: str = "medium") -> None:
        """Add task to current project."""
        if not self.current_project:
            print("❌ No current project. Create one first.")
            return
        
        # Use state from previous command
        project = self.projects[self.current_project]
        task = {
            'title': title,
            'priority': priority,
            'completed': False,
            'created_at': datetime.now()
        }
        
        project['tasks'].append(task)
        print(f"✅ Added task '{title}' to project '{self.current_project}'")
    
    def show_current_project(self) -> None:
        """Display current project information."""
        if not self.current_project:
            print("ℹ️  No current project selected")
            return
        
        project = self.projects[self.current_project]
        print(f"\\n📂 Current Project: {self.current_project}")
        print(f"Description: {project['description']}")
        print(f"Tasks: {len(project['tasks'])}")
        
        for task in project['tasks']:
            status = "✅" if task['completed'] else "⏳"
            print(f"  {status} {task['title']} ({task['priority']})")
```

### Configuration Management

```python
class ConfigurableApp:
    """App with persistent configuration."""
    
    def __init__(self):
        self.config = self._load_default_config()
        self.data_store = []
    
    def _load_default_config(self):
        return {
            'output_format': 'json',
            'verbose': False,
            'max_items': 100,
            'auto_backup': True
        }
    
    def set_config(self, key: str, value: str) -> None:
        """Set a configuration value."""
        if key not in self.config:
            print(f"❌ Unknown config key: {key}")
            print(f"Available keys: {list(self.config.keys())}")
            return
        
        # Type conversion based on existing value
        existing_type = type(self.config[key])
        
        try:
            if existing_type == bool:
                converted_value = value.lower() in ('true', '1', 'yes', 'on')
            elif existing_type == int:
                converted_value = int(value)
            else:
                converted_value = value
            
            self.config[key] = converted_value
            print(f"✅ Set {key} = {converted_value}")
            
        except ValueError:
            print(f"❌ Invalid value '{value}' for {key} (expected {existing_type.__name__})")
    
    def show_config(self) -> None:
        """Display current configuration."""
        print("\\n⚙️  Current Configuration:")
        for key, value in self.config.items():
            print(f"   {key}: {value}")
    
    def process_data(self, input_data: str) -> None:
        """Process data using current configuration."""
        # Configuration affects how processing works
        if self.config['verbose']:
            print(f"Processing with config: {self.config}")
        
        # Use configuration settings
        max_items = self.config['max_items']
        output_format = self.config['output_format']
        
        print(f"Processing {input_data} (max: {max_items}, format: {output_format})")
```

## Advanced Patterns

### Inheritance and Method Override

```python
class BaseApplication:
    """Base application class with common functionality."""
    
    def __init__(self):
        self.initialized = True
        self.log_level = "INFO"
    
    def show_version(self) -> None:
        """Show application version."""
        print("Base Application v1.0.0")
    
    def set_log_level(self, level: str = "INFO") -> None:
        """Set logging level."""
        self.log_level = level.upper()
        print(f"Log level set to: {self.log_level}")

class DatabaseApp(BaseApplication):
    """
    Database Application
    
    Extended application with database-specific functionality.
    """
    
    def __init__(self):
        super().__init__()
        self.connection = None
        self.connected_db = None
    
    def connect(self, host: str, database: str, port: int = 5432) -> None:
        """Connect to database."""
        print(f"Connecting to {database} at {host}:{port}")
        self.connected_db = database
        self.connection = f"mock_connection_{database}"
        print(f"✅ Connected to {database}")
    
    def show_version(self) -> None:
        """Show application version - overrides parent."""
        print("Database Application v2.1.0")
        print("Based on Base Application v1.0.0")
    
    def execute_query(self, sql: str, limit: int = 100) -> None:
        """Execute SQL query."""
        if not self.connection:
            print("❌ Not connected to database. Use 'connect' command first.")
            return
        
        print(f"Executing query on {self.connected_db}:")
        print(f"SQL: {sql}")
        print(f"Limit: {limit}")
        print("✅ Query executed successfully")
```

### Resource Management

```python
class FileManager:
    """File manager with resource cleanup."""
    
    def __init__(self):
        self.open_files = {}
        self.temp_files = []
    
    def open_file(self, file_path: str, mode: str = "r") -> None:
        """Open a file for operations."""
        try:
            handle = open(file_path, mode)
            self.open_files[file_path] = handle
            print(f"✅ Opened {file_path} in {mode} mode")
        except IOError as e:
            print(f"❌ Error opening {file_path}: {e}")
    
    def close_file(self, file_path: str) -> None:
        """Close an open file."""
        if file_path in self.open_files:
            self.open_files[file_path].close()
            del self.open_files[file_path]
            print(f"✅ Closed {file_path}")
        else:
            print(f"❌ File {file_path} not open")
    
    def list_open_files(self) -> None:
        """Show all currently open files."""
        if not self.open_files:
            print("ℹ️  No files currently open")
            return
        
        print(f"\\n📂 Open Files ({len(self.open_files)}):")
        for path, handle in self.open_files.items():
            print(f"   {path} ({handle.mode})")
    
    def cleanup(self) -> None:
        """Close all open files and clean up resources."""
        count = len(self.open_files)
        
        for file_path in list(self.open_files.keys()):
            self.close_file(file_path)
        
        # Clean up temp files
        for temp_file in self.temp_files:
            try:
                os.remove(temp_file)
                print(f"🗑️  Removed temp file: {temp_file}")
            except OSError:
                pass
        
        self.temp_files.clear()
        print(f"✅ Cleanup complete. Closed {count} files.")
```

## Best Practices

### 1. Constructor Design

```python
# ✅ Good: Simple initialization with sensible defaults
class GoodApp:
    """Well-designed application class."""
    
    def __init__(self):
        self.config = self._load_default_config()
        self.state = {}
        self.initialized = True
    
    def _load_default_config(self):
        return {
            'debug': False,
            'max_retries': 3,
            'timeout': 30
        }

# ❌ Avoid: Complex constructor with external dependencies
class BadApp:
    def __init__(self, db_url, api_key, config_file):  # Too many dependencies
        # Complex initialization that might fail
        pass
```

### 2. State Organization

```python
class WellOrganizedApp:
    """Example of good state organization."""
    
    def __init__(self):
        # Configuration (rarely changes)
        self.config = {
            'format': 'json',
            'verbose': False
        }
        
        # Runtime state (changes during execution)
        self.current_session = {
            'start_time': datetime.now(),
            'commands_run': 0,
            'last_command': None
        }
        
        # Data storage (accumulates over time)
        self.data_cache = {}
        self.operation_history = []
    
    def process_item(self, item: str) -> None:
        """Process an item and update state appropriately."""
        # Update session state
        self.current_session['commands_run'] += 1
        self.current_session['last_command'] = 'process_item'
        
        # Add to history
        self.operation_history.append({
            'operation': 'process_item',
            'item': item,
            'timestamp': datetime.now()
        })
        
        print(f"Processed: {item}")
```

### 3. Error Handling

```python
class RobustApp:
    """Example of good error handling in class-based CLI."""
    
    def __init__(self):
        self.connections = {}
        self.last_error = None
    
    def connect_service(self, service_name: str, url: str) -> None:
        """Connect to external service with proper error handling."""
        try:
            # Simulate connection
            if not url.startswith(('http://', 'https://')):
                raise ValueError("Invalid URL format")
            
            self.connections[service_name] = {
                'url': url,
                'connected_at': datetime.now(),
                'status': 'connected'
            }
            
            print(f"✅ Connected to {service_name}")
            
        except ValueError as e:
            self.last_error = str(e)
            print(f"❌ Connection failed: {e}")
            
        except Exception as e:
            self.last_error = f"Unexpected error: {str(e)}"
            print(f"❌ Unexpected error: {e}")
    
    def show_last_error(self) -> None:
        """Display the last error that occurred."""
        if self.last_error:
            print(f"🔍 Last Error: {self.last_error}")
        else:
            print("ℹ️  No recent errors")
```

### 4. Documentation and Help

```python
class DocumentedApp:
    """
    Well-Documented Application
    
    This application demonstrates proper documentation
    practices for class-based CLIs.
    """
    
    def __init__(self):
        self.items = []
    
    def add_item(
        self,
        name: str,
        category: str = "general",
        priority: int = 1,
        active: bool = True
    ) -> None:
        """
        Add a new item to the collection.
        
        Creates a new item with the specified properties and adds it
        to the internal collection. Items can be managed using other
        commands in this application.
        
        Args:
            name: The name/title of the item (must be unique)
            category: Category for organizing items (default: "general")  
            priority: Priority level from 1-10 (1=highest, default: 1)
            active: Whether the item is currently active (default: True)
            
        Examples:
            Add a simple item:
            $ app add-item --name "Important Task"
            
            Add with full details:
            $ app add-item --name "Database Backup" --category "maintenance" --priority 2
            
            Add inactive item:
            $ app add-item --name "Future Feature" --active False
        """
        # Validate inputs
        if any(item['name'] == name for item in self.items):
            print(f"❌ Item '{name}' already exists")
            return
        
        if not (1 <= priority <= 10):
            print(f"❌ Priority must be between 1-10 (got: {priority})")
            return
        
        # Create item
        item = {
            'name': name,
            'category': category,
            'priority': priority,
            'active': active,
            'created_at': datetime.now()
        }
        
        self.items.append(item)
        print(f"✅ Added item '{name}' to category '{category}'")
```

## See Also

- [Module-based CLI Guide](module-cli.md) - For functional approaches
- [Type Annotations](../features/type-annotations.md) - Detailed type system guide
- [Theme System](../features/themes.md) - Customizing appearance  
- [Complete Examples](../guides/examples.md) - More real-world examples
- [Best Practices](../guides/best-practices.md) - General CLI development tips

---

**Navigation**: [← Help Hub](help.md) | [Module-based Guide →](module-cli-guide.md)  
**Example**: [cls_example.py](../cls_example.py)
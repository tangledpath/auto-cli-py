# Mode Comparison

[← Back to User Guide](index.md) | [↑ Documentation Hub](../help.md)

## Overview

Auto-CLI-Py offers two distinct modes for creating CLIs. This guide provides a detailed comparison to help you choose the right approach.

## Quick Comparison Table

| Feature | Module-based | Class-based |
|---------|--------------|-------------|
| **Setup Complexity** | Simple | Moderate |
| **State Management** | No built-in state | Instance state |
| **Code Style** | Functional | Object-oriented |
| **Organization** | Functions in module | Methods in class |
| **Constructor Args** | N/A | Become global CLI args |
| **Best For** | Scripts, utilities | Applications, services |
| **Testing** | Test functions directly | Test methods on instance |
| **Command Structure** | Flat or hierarchical with `__` | Flat or with inner classes |

## Detailed Comparison

### State Management

**Module-based**: Stateless by design
```python
# Each function call is independent
def process_file(input_file: str, output_file: str) -> None:
    # Must open/close resources each time
    with open(input_file) as f:
        data = f.read()
    # Process and save
```

**Class-based**: Maintains state across command
```python
class FileProcessor:
    def __init__(self, cache_dir: str = "./cache"):
        self.cache_dir = cache_dir
        self.processed_files = set()
        self.connection = self.setup_connection()
    
    def process_file(self, input_file: str) -> None:
        # Can reuse connection and track state
        if input_file in self.processed_files:
            print("Already processed")
            return
        # Process using self.connection
        self.processed_files.add(input_file)
```

### Command Organization

**Module-based**: Uses double underscores for hierarchy
```python
# Creates command groups
def user__create(name: str, email: str) -> None:
    """Create user."""
    pass

def user__delete(user_id: str) -> None:
    """Delete user."""
    pass

# Usage: python cli.py user create --name John
```

**Class-based**: Uses inner classes with double-dash
```python
class AppCLI:
    class UserManagement:
        def create(self, name: str, email: str) -> None:
            """Create user."""
            pass
        
        def delete(self, user_id: str) -> None:
            """Delete user."""
            pass

# Usage: python cli.py user-management--create --name John
```

### Parameter Handling

**Module-based**: All parameters in function signature
```python
def deploy(
    environment: str,
    version: str = "latest",
    dry_run: bool = False
) -> None:
    """Deploy application."""
    pass

# Usage: python cli.py deploy --environment prod --version 1.2.3
```

**Class-based**: Constructor params become global args
```python
class Deployer:
    def __init__(self, environment: str = "dev", region: str = "us-east"):
        # These become global arguments
        self.environment = environment
        self.region = region
    
    def deploy(self, version: str = "latest", dry_run: bool = False) -> None:
        """Deploy to configured environment."""
        print(f"Deploying {version} to {self.environment} in {self.region}")

# Usage: python cli.py --environment prod --region eu-west deploy --version 1.2.3
```

### Initialization and Cleanup

**Module-based**: No built-in lifecycle
```python
# Must handle setup/teardown in each function
def backup_database(database: str, output: str) -> None:
    conn = connect_to_db(database)
    try:
        # Perform backup
        pass
    finally:
        conn.close()
```

**Class-based**: Constructor handles initialization
```python
class DatabaseManager:
    def __init__(self, host: str = "localhost"):
        self.connection = self.connect_to_db(host)
    
    def backup(self, output: str) -> None:
        # Connection already established
        self.connection.backup(output)
    
    def __del__(self):
        # Cleanup when done
        if hasattr(self, 'connection'):
            self.connection.close()
```

### Testing Approaches

**Module-based**: Direct function testing
```python
# test_module_cli.py
from my_cli import process_data

def test_process_data():
    result = process_data("input.csv", "output.json")
    assert result == 0
```

**Class-based**: Instance-based testing
```python
# test_class_cli.py
from my_cli import DataProcessor

def test_process_data():
    processor = DataProcessor(cache_enabled=False)
    result = processor.process("input.csv")
    assert result == 0
    assert processor.files_processed == 1
```

## Use Case Examples

### When to Use Module-based

**1. Simple Scripts**
```python
# File converter utility
def convert_json_to_csv(input_file: str, output_file: str) -> None:
    """Convert JSON to CSV format."""
    pass

def convert_csv_to_json(input_file: str, output_file: str) -> None:
    """Convert CSV to JSON format."""
    pass
```

**2. Stateless Operations**
```python
# Hash calculator
def calculate_hash(file_path: str, algorithm: str = "sha256") -> None:
    """Calculate file hash."""
    pass

def verify_hash(file_path: str, expected_hash: str) -> None:
    """Verify file hash matches expected value."""
    pass
```

### When to Use Class-based

**1. Database Applications**
```python
class DatabaseCLI:
    def __init__(self, connection_string: str = "sqlite:///app.db"):
        self.db = Database(connection_string)
        self.current_table = None
    
    def use_table(self, table_name: str) -> None:
        """Select table for operations."""
        self.current_table = table_name
    
    def query(self, sql: str) -> None:
        """Execute query on current table."""
        results = self.db.execute(sql, self.current_table)
```

**2. API Clients**
```python
class APIClient:
    def __init__(self, base_url: str = "https://api.example.com", timeout: int = 30):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.auth_token = None
    
    def login(self, username: str, password: str) -> None:
        """Authenticate with API."""
        self.auth_token = self._authenticate(username, password)
        self.session.headers['Authorization'] = f'Bearer {self.auth_token}'
    
    def get_data(self, endpoint: str) -> None:
        """Fetch data from authenticated endpoint."""
        response = self.session.get(f"{self.base_url}/{endpoint}")
```

## Migration Between Modes

### Module to Class

```python
# Before (module-based)
_connection = None

def connect(host: str, port: int = 5432) -> None:
    global _connection
    _connection = create_connection(host, port)

def query(sql: str) -> None:
    if not _connection:
        print("Not connected")
        return
    _connection.execute(sql)

# After (class-based)
class DatabaseCLI:
    def __init__(self, host: str = "localhost", port: int = 5432):
        self.connection = None
        self.host = host
        self.port = port
    
    def connect(self) -> None:
        self.connection = create_connection(self.host, self.port)
    
    def query(self, sql: str) -> None:
        if not self.connection:
            print("Not connected")
            return
        self.connection.execute(sql)
```

### Class to Module

```python
# Before (class-based)
class Calculator:
    def __init__(self):
        self.result = 0
    
    def add(self, x: float, y: float) -> None:
        self.result = x + y
        print(f"Result: {self.result}")

# After (module-based)
def add(x: float, y: float) -> None:
    result = x + y
    print(f"Result: {result}")
```

## Performance Considerations

### Module-based
- ✅ Faster startup (no class instantiation)
- ✅ Lower memory usage (no instance state)
- ❌ May repeat initialization for each command

### Class-based
- ❌ Slower startup (class instantiation)
- ❌ Higher memory usage (instance state)
- ✅ Reuses resources (connections, caches)

## Summary Recommendations

### Choose Module-based When:
- Building simple utilities or scripts
- Operations are independent and stateless
- Preferring functional programming style
- Quick CLI needed for existing functions
- Minimal setup/configuration required

### Choose Class-based When:
- Building complex applications
- Need persistent state between operations
- Managing resources (connections, files)
- Following object-oriented design
- Requiring initialization/cleanup logic

## See Also

- [Module CLI Guide](module-cli.md) - Complete module documentation
- [Class CLI Guide](class-cli.md) - Complete class documentation
- [Inner Classes Pattern](inner-classes.md) - Advanced class organization
- [Choosing CLI Mode](../getting-started/choosing-cli-mode.md) - Quick decision guide

---

**Navigation**: [← Inner Classes](inner-classes.md) | [User Guide →](index.md)
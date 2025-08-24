# Examples

[← Back to Guides](index.md) | [↑ Documentation Hub](../help.md)

## Real-World CLI Examples

This guide showcases complete, real-world examples of CLIs built with Auto-CLI-Py.

## File Processing Tool

A complete file processing utility with multiple operations:

```python
#!/usr/bin/env python3
"""File processing utility for common operations."""

import sys
from pathlib import Path
from typing import List, Optional
from enum import Enum
from auto_cli import CLI

class CompressionFormat(Enum):
    ZIP = "zip"
    TAR = "tar"
    GZIP = "gz"
    BZIP2 = "bz2"

class HashAlgorithm(Enum):
    MD5 = "md5"
    SHA1 = "sha1"
    SHA256 = "sha256"
    SHA512 = "sha512"

def compress_files(
    files: List[str],
    output: str,
    format: CompressionFormat = CompressionFormat.ZIP,
    level: int = 6,
    verbose: bool = False
) -> None:
    """
    Compress multiple files into an archive.
    
    Args:
        files: List of files to compress
        output: Output archive path
        format: Compression format to use
        level: Compression level (1-9, where 9 is maximum)
        verbose: Show detailed progress
        
    Examples:
        Compress files to ZIP:
        $ filetool compress-files file1.txt file2.txt --output archive.zip
        
        Create tar.gz with maximum compression:
        $ filetool compress-files *.log --output logs.tar.gz --format tar --level 9
    """
    if verbose:
        print(f"Compressing {len(files)} files to {output}")
        print(f"Format: {format.value}, Level: {level}")
    
    for file in files:
        if not Path(file).exists():
            print(f"❌ Error: File not found: {file}")
            return 1
    
    print(f"✅ Created {format.value} archive: {output}")
    return 0

def calculate_hash(
    file: str,
    algorithm: HashAlgorithm = HashAlgorithm.SHA256,
    compare_with: Optional[str] = None
) -> None:
    """
    Calculate cryptographic hash of a file.
    
    Args:
        file: File to hash
        algorithm: Hash algorithm to use
        compare_with: Optional hash to compare against
    """
    if not Path(file).exists():
        print(f"❌ Error: File not found: {file}")
        return 1
    
    # Simulate hash calculation
    calculated_hash = f"{algorithm.value}_hash_of_{Path(file).name}"
    print(f"{algorithm.value.upper()}: {calculated_hash}")
    
    if compare_with:
        if calculated_hash == compare_with:
            print("✅ Hash verification passed")
        else:
            print("❌ Hash verification failed")
            return 1
    
    return 0

def find_duplicates(
    directory: str,
    recursive: bool = True,
    min_size: int = 0,
    pattern: str = "*"
) -> None:
    """
    Find duplicate files in a directory.
    
    Args:
        directory: Directory to search
        recursive: Search subdirectories
        min_size: Minimum file size in bytes
        pattern: File pattern to match
    """
    path = Path(directory)
    if not path.is_dir():
        print(f"❌ Error: Not a directory: {directory}")
        return 1
    
    search_pattern = f"**/{pattern}" if recursive else pattern
    files = [f for f in path.glob(search_pattern) if f.is_file() and f.stat().st_size >= min_size]
    
    print(f"Scanning {len(files)} files for duplicates...")
    # Simulate duplicate detection
    print("✅ Found 3 duplicate groups:")
    print("  - file1.txt, backup/file1.txt (2.3 MB)")
    print("  - image.jpg, photos/image.jpg, archive/image.jpg (5.1 MB)")
    print("  - data.csv, old/data.csv (156 KB)")
    
    return 0

def batch_rename(
    pattern: str,
    replacement: str,
    directory: str = ".",
    dry_run: bool = True,
    case_sensitive: bool = True
) -> None:
    """
    Batch rename files using pattern matching.
    
    Args:
        pattern: Pattern to match in filenames
        replacement: Replacement string
        directory: Directory containing files
        dry_run: Show what would be renamed without doing it
        case_sensitive: Use case-sensitive matching
    """
    path = Path(directory)
    mode = "Would rename" if dry_run else "Renaming"
    
    # Simulate renaming
    examples = [
        ("old_file_001.txt", "new_file_001.txt"),
        ("old_file_002.txt", "new_file_002.txt"),
        ("old_document.pdf", "new_document.pdf")
    ]
    
    print(f"{mode} {len(examples)} files:")
    for old, new in examples:
        print(f"  {old} → {new}")
    
    if dry_run:
        print("\n💡 Use --no-dry-run to actually rename files")
    else:
        print("\n✅ Renamed 3 files successfully")
    
    return 0

if __name__ == '__main__':
    cli = CLI(
        sys.modules[__name__],
        title="FileTool - Advanced File Operations",
        theme_name="colorful"
    )
    cli.display()
```

## Database Manager CLI

A class-based database management tool:

```python
#!/usr/bin/env python3
"""Database management CLI with connection state."""

from auto_cli import CLI
from datetime import datetime
from typing import Optional, List
from enum import Enum

class BackupFormat(Enum):
    SQL = "sql"
    CUSTOM = "custom"
    TAR = "tar"
    DIRECTORY = "directory"

class DatabaseManager:
    """
    Database management tool with persistent connections.
    
    Manages database connections, backups, and maintenance tasks
    with support for multiple database types.
    """
    
    def __init__(self, default_host: str = "localhost", default_port: int = 5432):
        """
        Initialize database manager.
        
        Args:
            default_host: Default database host
            default_port: Default database port
        """
        self.default_host = default_host
        self.default_port = default_port
        self.connection = None
        self.connection_time = None
        self.history = []
    
    def connect(
        self,
        database: str,
        username: str,
        host: Optional[str] = None,
        port: Optional[int] = None,
        ssl: bool = True
    ) -> None:
        """
        Connect to a database.
        
        Args:
            database: Database name
            username: Username for authentication
            host: Database host (uses default if not specified)
            port: Database port (uses default if not specified)
            ssl: Use SSL connection
        """
        host = host or self.default_host
        port = port or self.default_port
        
        print(f"Connecting to {database} at {host}:{port} as {username}")
        if ssl:
            print("🔒 Using SSL connection")
        
        # Simulate connection
        self.connection = {
            'database': database,
            'host': host,
            'port': port,
            'username': username,
            'ssl': ssl
        }
        self.connection_time = datetime.now()
        
        self.history.append(f"Connected to {database} at {host}:{port}")
        print("✅ Connected successfully")
        return 0
    
    def disconnect(self) -> None:
        """Disconnect from the current database."""
        if not self.connection:
            print("⚠️ Not connected to any database")
            return 1
        
        db_info = f"{self.connection['database']} at {self.connection['host']}"
        print(f"Disconnecting from {db_info}")
        
        self.connection = None
        self.connection_time = None
        self.history.append(f"Disconnected from {db_info}")
        
        print("✅ Disconnected successfully")
        return 0
    
    def status(self) -> None:
        """Show current connection status and information."""
        print("=== Database Manager Status ===")
        
        if self.connection:
            print(f"✅ Connected to: {self.connection['database']}")
            print(f"   Host: {self.connection['host']}:{self.connection['port']}")
            print(f"   User: {self.connection['username']}")
            print(f"   SSL: {'Enabled' if self.connection['ssl'] else 'Disabled'}")
            
            if self.connection_time:
                duration = datetime.now() - self.connection_time
                print(f"   Connected for: {duration}")
        else:
            print("❌ Not connected")
        
        print(f"\nDefault host: {self.default_host}:{self.default_port}")
        print(f"History: {len(self.history)} operations")
        return 0
    
    class BackupOperations:
        """Database backup operations."""
        
        def __init__(self, backup_dir: str = "./backups", compress: bool = True):
            """
            Initialize backup operations.
            
            Args:
                backup_dir: Default backup directory
                compress: Compress backups by default
            """
            self.backup_dir = backup_dir
            self.compress = compress
        
        def create(
            self,
            output_file: Optional[str] = None,
            format: BackupFormat = BackupFormat.SQL,
            tables: Optional[List[str]] = None,
            exclude_tables: Optional[List[str]] = None
        ) -> None:
            """
            Create a database backup.
            
            Args:
                output_file: Backup file path (auto-generated if not specified)
                format: Backup format
                tables: Specific tables to backup (all if not specified)
                exclude_tables: Tables to exclude from backup
            """
            # Check connection
            if not hasattr(self, 'connection') or not self.connection:
                print("❌ Error: Not connected to any database")
                return 1
            
            # Generate filename if needed
            if not output_file:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                db_name = self.connection['database']
                output_file = f"{self.backup_dir}/{db_name}_{timestamp}.{format.value}"
            
            print(f"Creating backup of {self.connection['database']}")
            print(f"Format: {format.value}")
            print(f"Output: {output_file}")
            
            if tables:
                print(f"Tables: {', '.join(tables)}")
            elif exclude_tables:
                print(f"Excluding: {', '.join(exclude_tables)}")
            
            if self.compress:
                print("🗜️ Compression enabled")
            
            # Simulate backup
            print("📦 Backing up database...")
            print("✅ Backup completed successfully")
            
            return 0
        
        def restore(
            self,
            backup_file: str,
            target_database: Optional[str] = None,
            clean: bool = False,
            jobs: int = 1
        ) -> None:
            """
            Restore database from backup.
            
            Args:
                backup_file: Path to backup file
                target_database: Target database name (uses current if not specified)
                clean: Clean (drop) database objects before restore
                jobs: Number of parallel jobs for restore
            """
            if not hasattr(self, 'connection') or not self.connection:
                print("❌ Error: Not connected to any database")
                return 1
            
            target = target_database or self.connection['database']
            
            print(f"Restoring backup to {target}")
            print(f"Source: {backup_file}")
            
            if clean:
                print("⚠️ Will drop existing objects before restore")
            
            if jobs > 1:
                print(f"🚀 Using {jobs} parallel jobs")
            
            print("📥 Restoring database...")
            print("✅ Restore completed successfully")
            
            return 0
    
    def show_history(self, limit: int = 10) -> None:
        """
        Show command history.
        
        Args:
            limit: Maximum number of entries to show
        """
        if not self.history:
            print("No history available")
            return
        
        print(f"=== Last {limit} Operations ===")
        for i, entry in enumerate(self.history[-limit:], 1):
            print(f"{i}. {entry}")
        
        return 0

if __name__ == '__main__':
    cli = CLI(DatabaseManager, theme_name="colorful")
    cli.display()
```

## API Client Tool

A comprehensive API client with authentication:

```python
#!/usr/bin/env python3
"""RESTful API client with authentication and session management."""

from auto_cli import CLI
from typing import Optional, Dict, List
from enum import Enum
import json

class HTTPMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"

class OutputFormat(Enum):
    JSON = "json"
    TABLE = "table"
    RAW = "raw"
    PRETTY = "pretty"

class APIClient:
    """
    RESTful API client with authentication support.
    
    A command-line tool for interacting with REST APIs, managing
    authentication, and formatting responses.
    """
    
    def __init__(
        self,
        base_url: str = "https://api.example.com",
        timeout: int = 30,
        verify_ssl: bool = True
    ):
        """
        Initialize API client.
        
        Args:
            base_url: Base URL for API requests
            timeout: Request timeout in seconds
            verify_ssl: Verify SSL certificates
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.auth_token = None
        self.headers = {
            'User-Agent': 'auto-cli-py/1.0',
            'Accept': 'application/json'
        }
    
    def login(
        self,
        username: str,
        password: Optional[str] = None,
        token: Optional[str] = None,
        endpoint: str = "/auth/login"
    ) -> None:
        """
        Authenticate with the API.
        
        Args:
            username: Username or email
            password: Password (will prompt if not provided)
            token: Use token directly instead of username/password
            endpoint: Authentication endpoint
        """
        if token:
            self.auth_token = token
            self.headers['Authorization'] = f'Bearer {token}'
            print("✅ Authenticated with provided token")
            return 0
        
        print(f"Authenticating as {username}...")
        
        # Simulate authentication
        self.auth_token = "example_auth_token_12345"
        self.headers['Authorization'] = f'Bearer {self.auth_token}'
        
        print("✅ Authentication successful")
        return 0
    
    def request(
        self,
        endpoint: str,
        method: HTTPMethod = HTTPMethod.GET,
        data: Optional[str] = None,
        params: Optional[List[str]] = None,
        output: OutputFormat = OutputFormat.PRETTY
    ) -> None:
        """
        Make an API request.
        
        Args:
            endpoint: API endpoint path
            method: HTTP method
            data: Request body (JSON string)
            params: Query parameters as key=value pairs
            output: Output format for response
            
        Examples:
            GET request:
            $ api request /users --params page=1 limit=10
            
            POST request with data:
            $ api request /users --method POST --data '{"name": "John"}'
        """
        if not endpoint.startswith('/'):
            endpoint = '/' + endpoint
        
        url = f"{self.base_url}{endpoint}"
        
        print(f"{method.value} {url}")
        
        if params:
            param_dict = {}
            for param in params:
                if '=' in param:
                    key, value = param.split('=', 1)
                    param_dict[key] = value
            print(f"Parameters: {param_dict}")
        
        if data:
            print(f"Body: {data}")
        
        # Simulate response
        response_data = {
            "status": "success",
            "data": {
                "id": 123,
                "name": "Example Response",
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }
        
        print("\n📥 Response:")
        
        if output == OutputFormat.PRETTY:
            print(json.dumps(response_data, indent=2))
        elif output == OutputFormat.TABLE:
            print("┌─────────┬──────────────────┐")
            print("│ Field   │ Value            │")
            print("├─────────┼──────────────────┤")
            print("│ status  │ success          │")
            print("│ id      │ 123              │")
            print("│ name    │ Example Response │")
            print("└─────────┴──────────────────┘")
        else:
            print(response_data)
        
        return 0
    
    class Resources:
        """Common resource operations."""
        
        def list_items(
            self,
            resource: str,
            page: int = 1,
            limit: int = 20,
            sort: Optional[str] = None,
            filter: Optional[List[str]] = None
        ) -> None:
            """
            List resources with pagination.
            
            Args:
                resource: Resource type (users, posts, etc.)
                page: Page number
                limit: Items per page
                sort: Sort field (prefix with - for descending)
                filter: Filter conditions as field=value pairs
            """
            print(f"Listing {resource} (page {page}, limit {limit})")
            
            if sort:
                direction = "DESC" if sort.startswith('-') else "ASC"
                field = sort.lstrip('-')
                print(f"Sort: {field} {direction}")
            
            if filter:
                print(f"Filters: {filter}")
            
            # Simulate listing
            print(f"\n📋 Found 3 {resource}:")
            print("1. Item One (ID: 101)")
            print("2. Item Two (ID: 102)")
            print("3. Item Three (ID: 103)")
            
            print(f"\nPage {page} of 5 (Total: 87 items)")
            
            return 0
        
        def get_item(
            self,
            resource: str,
            id: str,
            expand: Optional[List[str]] = None
        ) -> None:
            """
            Get a specific resource by ID.
            
            Args:
                resource: Resource type
                id: Resource ID
                expand: Related resources to include
            """
            print(f"Fetching {resource}/{id}")
            
            if expand:
                print(f"Expanding: {', '.join(expand)}")
            
            # Simulate response
            print(f"\n📄 {resource.title()} Details:")
            print(f"ID: {id}")
            print(f"Name: Example {resource.title()}")
            print(f"Created: 2024-01-15")
            print(f"Status: Active")
            
            return 0
    
    def show_config(self) -> None:
        """Display current client configuration."""
        print("=== API Client Configuration ===")
        print(f"Base URL: {self.base_url}")
        print(f"Timeout: {self.timeout}s")
        print(f"SSL Verification: {'Enabled' if self.verify_ssl else 'Disabled'}")
        print(f"Authenticated: {'Yes' if self.auth_token else 'No'}")
        
        if self.headers:
            print("\nHeaders:")
            for key, value in self.headers.items():
                if key == 'Authorization' and value:
                    value = value[:20] + '...' if len(value) > 20 else value
                print(f"  {key}: {value}")
        
        return 0

if __name__ == '__main__':
    cli = CLI(APIClient, theme_name="colorful")
    cli.display()
```

## Usage Examples

### File Tool Usage
```bash
# Compress files
python filetool.py compress-files *.txt --output archive.zip --verbose

# Calculate hash
python filetool.py calculate-hash large_file.iso --algorithm sha256

# Find duplicates
python filetool.py find-duplicates ~/Documents --min-size 1048576

# Batch rename
python filetool.py batch-rename "old_" "new_" --no-dry-run
```

### Database Manager Usage
```bash
# Connect to database
python dbmanager.py connect mydb --username admin --host db.example.com

# Check status
python dbmanager.py status

# Create backup
python dbmanager.py backup-operations--create --format custom --compress

# Restore backup
python dbmanager.py backup-operations--restore backup.sql --clean --jobs 4
```

### API Client Usage
```bash
# Authenticate
python apiclient.py login --username user@example.com

# Make requests
python apiclient.py request /users --params page=2 limit=50
python apiclient.py request /users --method POST --data '{"name": "New User"}'

# Use resource commands
python apiclient.py resources--list-items users --sort -created_at --limit 100
python apiclient.py resources--get-item users 12345 --expand groups permissions
```

## See Also

- [Best Practices](best-practices.md) - Design patterns
- [Module CLI Guide](../user-guide/module-cli.md) - Module-based examples
- [Class CLI Guide](../user-guide/class-cli.md) - Class-based examples

---

**Navigation**: [← Best Practices](best-practices.md) | [Guides Index →](index.md)
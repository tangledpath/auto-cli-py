# Inner Classes Pattern

[← Back to User Guide](index.md) | [↑ Documentation Hub](../help.md)

## Overview

The inner classes pattern in Auto-CLI-Py provides a way to organize related commands while maintaining a flat command structure. Commands from inner classes are accessed using double-dash notation (e.g., `outer-class--inner-method`).

## Key Concepts

### Flat Command Structure
All commands remain flat - there are no hierarchical command groups. Inner class methods become commands with double-dash notation:

```bash
# All commands are at the same level
python cli.py --help                                    # Show all commands
python cli.py project-operations--create --name "app"  # Inner class method
python cli.py task-management--add --title "Task"      # Another inner class method
python cli.py generate-report --format json             # Main class method
```

### Global and Sub-Global Arguments

**Global Arguments**: Main class constructor parameters
```python
class ProjectManager:
    def __init__(self, config_file: str = "config.json", debug: bool = False):
        # These become global arguments available to all commands
        self.config_file = config_file
        self.debug = debug
```

**Sub-Global Arguments**: Inner class constructor parameters
```python
class ProjectManager:
    class ProjectOperations:
        def __init__(self, workspace: str = "./projects", auto_save: bool = True):
            # These become sub-global arguments for this inner class's commands
            self.workspace = workspace
            self.auto_save = auto_save
```

## Complete Example

```python
from auto_cli import CLI
from pathlib import Path
from typing import List

class ProjectManager:
    """Project Management CLI with organized flat commands."""
    
    def __init__(self, config_file: str = "config.json", debug: bool = False):
        """Initialize with global settings.
        
        Args:
            config_file: Configuration file path (global argument)
            debug: Enable debug mode (global argument)
        """
        self.config_file = config_file
        self.debug = debug
        self.projects = {}
        self._load_config()
    
    def _load_config(self):
        """Load configuration from file."""
        if self.debug:
            print(f"Loading config from {self.config_file}")
    
    def status(self) -> None:
        """Show overall system status."""
        print(f"Configuration: {self.config_file}")
        print(f"Debug mode: {'ON' if self.debug else 'OFF'}")
        print(f"Total projects: {len(self.projects)}")
    
    class ProjectOperations:
        """Project creation and management operations."""
        
        def __init__(self, workspace: str = "./projects", auto_save: bool = True):
            """Initialize project operations.
            
            Args:
                workspace: Workspace directory (sub-global argument)
                auto_save: Auto-save changes (sub-global argument)
            """
            self.workspace = Path(workspace)
            self.auto_save = auto_save
        
        def create(self, name: str, template: str = "default", tags: List[str] = None) -> None:
            """Create a new project.
            
            Args:
                name: Project name
                template: Project template to use
                tags: Tags for categorization
            """
            print(f"Creating project '{name}' in {self.workspace}")
            print(f"Using template: {template}")
            if tags:
                print(f"Tags: {', '.join(tags)}")
            if self.auto_save:
                print("✅ Auto-save enabled")
        
        def delete(self, project_id: str, force: bool = False) -> None:
            """Delete an existing project.
            
            Args:
                project_id: ID of project to delete
                force: Skip confirmation
            """
            if not force:
                print(f"Would delete project {project_id} from {self.workspace}")
                print("Use --force to confirm deletion")
            else:
                print(f"Deleting project {project_id}")
        
        def list_projects(self, filter_tag: str = None, show_archived: bool = False) -> None:
            """List all projects in workspace.
            
            Args:
                filter_tag: Filter by tag
                show_archived: Include archived projects
            """
            print(f"Listing projects in {self.workspace}")
            if filter_tag:
                print(f"Filter: tag='{filter_tag}'")
            print(f"Show archived: {show_archived}")
    
    class TaskManagement:
        """Task operations within projects."""
        
        def __init__(self, default_priority: str = "medium", notify: bool = True):
            """Initialize task management.
            
            Args:
                default_priority: Default priority for new tasks
                notify: Send notifications on changes
            """
            self.default_priority = default_priority
            self.notify = notify
        
        def add(self, title: str, project: str, priority: str = None, assignee: str = None) -> None:
            """Add task to project.
            
            Args:
                title: Task title
                project: Project ID
                priority: Task priority (uses default if not specified)
                assignee: Person assigned to task
            """
            priority = priority or self.default_priority
            print(f"Adding task to project {project}")
            print(f"Title: {title}")
            print(f"Priority: {priority}")
            if assignee:
                print(f"Assigned to: {assignee}")
            if self.notify:
                print("📧 Notification sent")
        
        def update(self, task_id: str, status: str, comment: str = None) -> None:
            """Update task status.
            
            Args:
                task_id: Task identifier
                status: New status
                comment: Optional comment
            """
            print(f"Updating task {task_id}")
            print(f"New status: {status}")
            if comment:
                print(f"Comment: {comment}")
    
    class ReportGeneration:
        """Report generation without sub-global arguments."""
        
        def summary(self, format: str = "text", detailed: bool = False) -> None:
            """Generate project summary report.
            
            Args:
                format: Output format (text, json, html)
                detailed: Include detailed statistics
            """
            print(f"Generating {'detailed' if detailed else 'basic'} summary")
            print(f"Format: {format}")
        
        def export(self, output_file: Path, include_tasks: bool = True) -> None:
            """Export project data.
            
            Args:
                output_file: Output file path
                include_tasks: Include task data in export
            """
            print(f"Exporting to {output_file}")
            print(f"Include tasks: {include_tasks}")

if __name__ == '__main__':
    cli = CLI(ProjectManager, theme_name="colorful")
    cli.display()
```

## Usage Examples

### Basic Usage
```bash
# Show all available commands (flat structure)
python project_mgr.py --help

# Main class method
python project_mgr.py status

# Inner class methods with double-dash notation
python project_mgr.py project-operations--create --name "web-app"
python project_mgr.py task-management--add --title "Setup CI/CD" --project "web-app"
python project_mgr.py report-generation--summary --format json --detailed
```

### With Global Arguments
```bash
# Global arguments apply to all commands
python project_mgr.py --config-file prod.json --debug status
python project_mgr.py --debug project-operations--list-projects
```

### With Sub-Global Arguments
```bash
# Sub-global arguments for specific inner class
python project_mgr.py project-operations--create \
    --workspace /prod/projects \
    --auto-save \
    --name "api-service" \
    --template "microservice"

python project_mgr.py task-management--add \
    --default-priority high \
    --no-notify \
    --title "Security audit" \
    --project "api-service"
```

### Complete Command Example
```bash
# Combining global, sub-global, and method arguments
python project_mgr.py \
    --config-file production.json \
    --debug \
    project-operations--create \
    --workspace /var/projects \
    --no-auto-save \
    --name "data-pipeline" \
    --template "etl" \
    --tags analytics ml production
```

## Design Guidelines

### When to Use Inner Classes

Use inner classes when you have:
- **Logically related commands** that share configuration
- **Commands that need sub-global arguments**
- **Better organization** without hierarchical nesting
- **Cleaner command grouping** in help output

### Best Practices

1. **Keep inner classes focused** - Each inner class should represent a cohesive set of operations
2. **Use descriptive class names** - They become part of the command name
3. **Document sub-global arguments** - Explain how they affect all methods in the class
4. **Limit nesting depth** - Only one level of inner classes is supported
5. **Consider flat methods** - Not everything needs to be in an inner class

### Naming Conventions

- **Inner class names**: Use CamelCase (e.g., `ProjectOperations`)
- **Method names**: Use snake_case (e.g., `list_projects`)
- **Generated commands**: Automatic kebab-case (e.g., `project-operations--list-projects`)

## Comparison with Module Hierarchies

Module-based CLIs use double underscores for hierarchies:
```python
# Module function
def project__create(name: str) -> None:
    pass

# Usage: python cli.py project create --name "app"
```

Class-based CLIs use inner classes with double-dash notation:
```python
# Inner class method
class CLI:
    class Project:
        def create(self, name: str) -> None:
            pass

# Usage: python cli.py project--create --name "app"
```

## Limitations

- Only one level of inner classes is supported
- Inner classes cannot have their own inner classes
- All commands remain flat (no true command groups)
- Constructor parameters must have defaults

## See Also

- [Class CLI Guide](class-cli.md) - Complete class-based CLI documentation
- [Module CLI Guide](module-cli.md) - Module-based alternative
- [Mode Comparison](mode-comparison.md) - Choosing between approaches
- [Best Practices](../guides/best-practices.md) - General guidelines

---

**Navigation**: [← Class CLI](class-cli.md) | [Mode Comparison →](mode-comparison.md)
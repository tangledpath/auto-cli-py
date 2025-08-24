# Quick Start Guide

[← Back to Help](../help.md) | [📦 Installation](installation.md) | [📖 Basic Usage](basic-usage.md)

## Table of Contents
- [Installation](#installation)
- [5-Minute Introduction](#5-minute-introduction)
- [Choose Your Mode](#choose-your-mode)
- [Module-based Example](#module-based-example)
- [Class-based Example](#class-based-example)
- [Key Features Demonstrated](#key-features-demonstrated)
- [Next Steps](#next-steps)

## Installation



## 5-Minute Introduction

Auto-CLI-Py automatically creates complete command-line interfaces from your existing Python code. Just add type annotations to your functions or methods, and you get a fully-featured CLI with argument parsing, help text, and type validation.

**Two ways to create CLIs:**
- **Module-based**: Perfect for utilities and functional code
- **Class-based**: Ideal for stateful applications and object-oriented designs
- 

## Installation

```bash
pip install auto-cli-py
```

That's it! No dependencies, works with Python 3.8+.

## Choose Your Mode

### When to use Module-based CLI
✅ Simple utilities and scripts  
✅ Functional programming style  
✅ Stateless operations  
✅ Quick prototypes  

### When to use Class-based CLI  
✅ Stateful applications  
✅ Object-oriented design  
✅ Complex workflows  
✅ Configuration management  

## Module-based Example

Create a file `my_tool.py`:

```python
from auto_cli import CLI
import sys

def greet(name: str = "World", excited: bool = False) -> None:
    """Greet someone by name."""
    greeting = f"Hello, {name}!"
    if excited:
        greeting += " 🎉"
    print(greeting)

def count_words(text: str, ignore_case: bool = True) -> None:
    """Count words in the given text."""
    if ignore_case:
        text = text.lower()
    
    words = text.split()
    print(f"Word count: {len(words)}")
    print(f"Unique words: {len(set(words))}")

if __name__ == '__main__':
    cli = CLI.from_module(sys.modules[__name__], title="My Tool")
    cli.display()
```

**Usage:**
```bash
python my_tool.py --help
python my_tool.py greet --name "Alice" --excited
python my_tool.py count-words --text "Hello world hello" --ignore-case
```

## Class-based Example

Create a file `my_app.py`:

```python
from auto_cli import CLI
from typing import List

class TaskManager:
    """Task Management Application
    
    A simple CLI for managing your daily tasks.
    """
    
    def __init__(self):
        self.tasks = []
        self.next_id = 1
    
    def add_task(self, title: str, priority: str = "medium") -> None:
        """Add a new task."""
        task = {
            'id': self.next_id,
            'title': title,
            'priority': priority,
            'completed': False
        }
        self.tasks.append(task)
        self.next_id += 1
        print(f"✅ Added task: {title} (priority: {priority})")
    
    def list_tasks(self, show_completed: bool = False) -> None:
        """List all tasks."""
        tasks_to_show = self.tasks
        if not show_completed:
            tasks_to_show = [t for t in tasks_to_show if not t['completed']]
        
        if not tasks_to_show:
            print("No tasks found.")
            return
        
        print(f"\\nTasks ({len(tasks_to_show)}):")
        for task in tasks_to_show:
            status = "✅" if task['completed'] else "⏳"
            print(f"{status} {task['id']}: {task['title']} [{task['priority']}]")
    
    def complete_task(self, task_id: int) -> None:
        """Mark a task as completed."""
        for task in self.tasks:
            if task['id'] == task_id:
                task['completed'] = True
                print(f"✅ Completed: {task['title']}")
                return
        
        print(f"❌ Task {task_id} not found")

if __name__ == '__main__':
    cli = CLI.from_class(TaskManager, theme_name="colorful")
    cli.display()
```

**Usage:**
```bash
python my_app.py --help
python my_app.py add-task --title "Learn Auto-CLI-Py" --priority "high"
python my_app.py add-task --title "Write documentation"
python my_app.py list-tasks
python my_app.py complete-task --task-id 1
python my_app.py list-tasks --show-completed
```

## Key Features Demonstrated

Both examples automatically provide:

### 🔧 **Automatic Argument Parsing**
- `str` parameters become `--name VALUE`
- `bool` parameters become flags `--excited`  
- `int` parameters become `--count 42`
- Default values are preserved

### 📚 **Help Generation**
- Function/method docstrings become command descriptions
- Parameter names become option names (with kebab-case conversion)
- Type information is included in help text

### ✨ **Built-in Features**
- Input validation based on type annotations
- Colorful output with customizable themes
- Shell completion support
- Error handling and user-friendly messages

### 🎨 **Themes and Customization**
```python
# Choose from built-in themes
cli = CLI.from_module(module, theme_name="colorful")
cli = CLI.from_class(MyClass, theme_name="universal") 

# Disable colors
cli = CLI.from_module(module, no_color=True)
```

## Next Steps

### 📖 Learn More
- **[Module-based CLI Guide](../module-cli-guide.md)** - Complete guide for function-based CLIs
- **[Class-based CLI Guide](../class-cli-guide.md)** - Complete guide for method-based CLIs  
- **[Installation Guide](installation.md)** - Detailed setup instructions
- **[Basic Usage](basic-usage.md)** - Core concepts and patterns

### 🚀 Advanced Features
- **[Type Annotations](../features/type-annotations.md)** - Supported types and validation
- **[Theme System](../features/themes.md)** - Customize colors and appearance
- **[Autocompletion](../features/autocompletion.md)** - Shell completion setup

### 💡 Examples and Inspiration
- **[Complete Examples](../guides/examples.md)** - Real-world usage patterns
- **[Best Practices](../guides/best-practices.md)** - Recommended approaches

---

**Navigation**: [← Help Hub](../help.md) | [Installation →](installation.md) | [Basic Usage →](basic-usage.md)  
**Examples**: [Module Example](../../mod_example.py) | [Class Example](../../cls_example.py)

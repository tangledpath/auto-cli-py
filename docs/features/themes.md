# Theme System

[← Back to Features](index.md) | [↑ Documentation Hub](../help.md)

## Overview

Auto-CLI-Py includes a built-in theme system that allows you to customize the appearance of your CLI output.

## Built-in Themes

### Universal Theme (Default)
A clean, minimal theme that works well in all terminals:
- Uses standard colors
- High contrast
- Accessible design
- Works with light and dark terminals

### Colorful Theme
A vibrant theme with rich colors:
- Bold, colorful output
- Enhanced visual hierarchy
- Best for modern terminals
- Optimized for dark backgrounds

## Using Themes

### Setting Theme
```python
from auto_cli import CLI

# Module-based CLI with theme
cli = CLI(sys.modules[__name__], theme_name="colorful")

# Class-based CLI with theme
cli = CLI(MyClass, theme_name="universal")
```

### Disabling Colors
```python
# Programmatically
cli = CLI(MyClass, no_color=True)

# Via environment variable
export NO_COLOR=1
python my_cli.py --help
```

## Theme Tuner

The theme tuner is a built-in command that helps you preview and adjust themes:

```bash
# Enable theme tuner in your CLI
cli = CLI(MyClass, theme_tuner=True)

# Use the tuner
python my_cli.py theme-tuner
```

## Creating Custom Themes

Coming soon: Custom theme creation guide.

## Color Support

Auto-CLI-Py respects terminal capabilities:
- Automatically detects color support
- Honors NO_COLOR environment variable
- Gracefully degrades on limited terminals
- Supports 8, 16, and 256 color modes

## See Also

- [Shell Completion](shell-completion.md) - Tab completion setup
- [Error Handling](error-handling.md) - Error message styling
- [Best Practices](../guides/best-practices.md) - UI/UX guidelines

---

**Navigation**: [← Features](index.md) | [Type Annotations →](type-annotations.md)
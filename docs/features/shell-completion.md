# Shell Completion

[← Back to Features](index.md) | [↑ Documentation Hub](../help.md)

## Overview

Auto-CLI-Py provides automatic shell completion for all generated CLIs, supporting Bash, Zsh, and Fish shells.

## Enabling Completion

Completion is enabled by default. To disable:
```python
cli = CLI(MyClass, completion=False)
```

## Setup by Shell

### Bash
```bash
# Add to ~/.bashrc
eval "$(_MY_CLI_PY_COMPLETE=source_bash my-cli)"

# Or for system-wide installation
my-cli --print-completion bash > /etc/bash_completion.d/my-cli
```

### Zsh
```bash
# Add to ~/.zshrc
eval "$(_MY_CLI_PY_COMPLETE=source_zsh my-cli)"

# Or add to fpath
my-cli --print-completion zsh > ~/.zfunc/_my-cli
```

### Fish
```bash
# Add to ~/.config/fish/completions/
my-cli --print-completion fish > ~/.config/fish/completions/my-cli.fish
```

## Features

### Command Completion
- All command names
- Command groups (for hierarchical CLIs)
- Command aliases

### Argument Completion
- Option names (--help, --version)
- Enum choices
- File and directory paths
- Custom completers

### Smart Suggestions
- Context-aware completions
- Type-based suggestions
- Recently used values

## Testing Completion

```bash
# Type command and press TAB
my-cli <TAB>
my-cli com<TAB>
my-cli command --<TAB>
```

## Troubleshooting

### Completion Not Working
1. Ensure shell completion is installed
2. Restart your shell or source config
3. Check completion is enabled in CLI
4. Verify shell type detection

### Debugging
```bash
# Check if completion is registered
complete -p | grep my-cli  # Bash
print -l $_comps | grep my-cli  # Zsh
```

## Custom Completers

Coming soon: Guide for custom completion logic.

## See Also

- [Type Annotations](type-annotations.md) - Types affect completion
- [Troubleshooting](../guides/troubleshooting.md) - Common issues
- [Best Practices](../guides/best-practices.md) - Completion tips

---

**Navigation**: [← Themes](themes.md) | [Error Handling →](error-handling.md)
# Contributing to Auto-CLI-Py

[← Back to Development](index.md) | [↑ Documentation Hub](../help.md)

## Welcome Contributors!

We're excited that you're interested in contributing to Auto-CLI-Py! This guide will help you get started.

## Code of Conduct

Please read and follow our code of conduct to ensure a welcoming environment for all contributors.

## Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/auto-cli-py.git
cd auto-cli-py
```

### 2. Set Up Development Environment

```bash
# Install Poetry if you haven't already
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install --with dev

# Install pre-commit hooks
poetry run pre-commit install
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

## Development Workflow

### 1. Make Your Changes

Follow these guidelines:
- Write clear, documented code
- Add type hints to all functions
- Include docstrings for modules, classes, and functions
- Follow existing code style

### 2. Write Tests

```bash
# Run tests
poetry run pytest

# Run specific test
poetry run pytest tests/test_cli.py::test_function_name

# Run with coverage
poetry run pytest --cov=auto_cli --cov-report=html
```

### 3. Check Code Quality

```bash
# Run all checks
./bin/lint.sh

# Or individually:
poetry run black auto_cli tests
poetry run ruff check auto_cli tests
poetry run mypy auto_cli
```

### 4. Update Documentation

- Update relevant documentation in `docs/`
- Add docstrings to new functions/classes
- Update CHANGELOG.md if applicable

## Submitting Changes

### 1. Commit Your Changes

```bash
# Use conventional commit format
git commit -m "feat: add new feature X"
git commit -m "fix: resolve issue with Y"
git commit -m "docs: update contributing guide"
```

### 2. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 3. Create Pull Request

- Go to GitHub and create a pull request
- Fill out the PR template completely
- Link any related issues
- Wait for review and address feedback

## Pull Request Guidelines

### PR Title Format
- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `test:` Test additions/changes
- `refactor:` Code refactoring
- `chore:` Maintenance tasks

### PR Description Should Include
- What changes were made
- Why the changes are needed
- How to test the changes
- Any breaking changes

## Testing Guidelines

### Test Structure
```python
def test_function_name():
    """Test description."""
    # Arrange
    input_data = "test"
    
    # Act
    result = function_under_test(input_data)
    
    # Assert
    assert result == expected_value
```

### Test Coverage
- Aim for >90% test coverage
- Test edge cases and error conditions
- Include integration tests for CLI behavior

## Code Style

### Python Style
- Follow PEP 8 (enforced by Black)
- Use meaningful variable names
- Keep functions focused and small

### Type Hints
```python
from typing import List, Optional, Union

def process_data(
    input_file: str,
    output_format: str = "json",
    filters: Optional[List[str]] = None
) -> Union[dict, str]:
    """Process data with optional filters."""
    pass
```

### Docstrings
```python
def example_function(param1: str, param2: int = 10) -> bool:
    """
    Brief description of function.
    
    Longer description if needed, explaining behavior,
    edge cases, or important details.
    
    Args:
        param1: Description of param1
        param2: Description of param2 with default
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param1 is empty
        
    Example:
        >>> example_function("test", 20)
        True
    """
    pass
```

## Areas for Contribution

### Good First Issues
- Look for issues labeled `good first issue`
- Documentation improvements
- Test coverage improvements
- Simple bug fixes

### Feature Requests
- Check existing issues first
- Discuss in an issue before implementing
- Consider backward compatibility

### Documentation
- Fix typos and improve clarity
- Add examples
- Translate documentation

## Review Process

### What to Expect
1. Automated checks run on your PR
2. Maintainer review (usually within 48 hours)
3. Feedback and requested changes
4. Approval and merge

### Review Criteria
- Code quality and style
- Test coverage
- Documentation updates
- Backward compatibility
- Performance impact

## Release Process

1. Maintainers handle releases
2. Semantic versioning is used
3. CHANGELOG.md is updated
4. PyPI package is published

## Getting Help

### Resources
- [GitHub Issues](https://github.com/tangledpath/auto-cli-py/issues)
- [Discussions](https://github.com/tangledpath/auto-cli-py/discussions)
- Review existing code and tests

### Questions?
- Open a discussion for general questions
- Comment on issues for specific problems
- Tag maintainers for urgent issues

## Recognition

Contributors are recognized in:
- GitHub contributors page
- AUTHORS file
- Release notes

## Thank You!

Your contributions help make Auto-CLI-Py better for everyone. We appreciate your time and effort!

---

**Navigation**: [← Development](index.md) | [Architecture →](architecture.md)
# Development

[↑ Documentation Hub](../help.md)

Documentation for contributors and developers working on Auto-CLI-Py.

## For Contributors

### 🤝 [Contributing](contributing.md)
How to contribute to Auto-CLI-Py.
- Setting up development environment
- Code style guidelines
- Submitting pull requests
- Issue reporting guidelines
- Community standards

### 🏗️ [Architecture](architecture.md)
Understanding the codebase structure.
- Project organization
- Core components
- Design decisions
- Extension points
- Future roadmap

### 🧪 [Testing](testing.md)
Testing guidelines and strategies.
- Running the test suite
- Writing new tests
- Test organization
- Coverage requirements
- CI/CD pipeline

### 📦 [Release Process](release-process.md)
How releases are managed.
- Version numbering
- Release checklist
- Publishing to PyPI
- Documentation updates
- Announcement process

## Quick Start for Contributors

### Development Setup
```bash
# Clone the repository
git clone https://github.com/tangledpath/auto-cli-py.git
cd auto-cli-py

# Install development dependencies
poetry install --with dev

# Run tests
poetry run pytest

# Run linters
poetry run ruff check .
poetry run mypy auto_cli

# Install pre-commit hooks
poetry run pre-commit install
```

### Project Structure
```
auto-cli-py/
├── auto_cli/          # Source code
│   ├── __init__.py
│   └── cli.py
├── tests/             # Test suite
│   ├── conftest.py
│   └── test_*.py
├── docs/              # Documentation
├── examples/          # Example CLIs
├── pyproject.toml     # Project configuration
└── README.md          # Project README
```

### Key Development Commands

**Testing**
```bash
# Run all tests with coverage
./bin/test.sh

# Run specific test file
poetry run pytest tests/test_cli.py -v

# Run with debugging
poetry run pytest -vv --tb=short
```

**Code Quality**
```bash
# Run all checks
./bin/lint.sh

# Format code
poetry run black auto_cli tests

# Type checking
poetry run mypy auto_cli --strict
```

**Building**
```bash
# Build distribution packages
poetry build

# Install locally for testing
poetry install
```

## Development Guidelines

### Code Style
- Follow PEP 8 with Black formatting
- Use type hints for all functions
- Write descriptive docstrings
- Keep functions focused and testable

### Commit Messages
- Use conventional commits format
- Include issue numbers when applicable
- Write clear, descriptive messages
- Separate concerns in commits

### Testing Philosophy
- Write tests for new features
- Maintain high test coverage (>90%)
- Test edge cases and errors
- Use fixtures for common setups

## Getting Help

### For Contributors
- Open a [Discussion](https://github.com/tangledpath/auto-cli-py/discussions) for questions
- Join our [Discord](#) community (coming soon)
- Check existing [Issues](https://github.com/tangledpath/auto-cli-py/issues)
- Read the [Architecture](architecture.md) guide

### Maintainer Contacts
- **Steven** - Project Lead
- **Contributors** - See [AUTHORS](https://github.com/tangledpath/auto-cli-py/blob/main/AUTHORS)

## Next Steps

- Read [Contributing Guidelines](contributing.md)
- Understand the [Architecture](architecture.md)
- Set up [Testing](testing.md)
- Learn the [Release Process](release-process.md)

---

**Ready to contribute?** Check out [good first issues](https://github.com/tangledpath/auto-cli-py/labels/good%20first%20issue)
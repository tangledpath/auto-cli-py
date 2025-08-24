#!/bin/bash
# Development environment setup script

set -e

echo "🚀 Setting up development environment for auto-cli-py..."

# Install dependencies
echo "📦 Installing dependencies with Poetry..."
poetry install --with dev

# Install pre-commit hooks
echo "🪝 Installing pre-commit hooks..."
poetry run pre-commit install

# Verify Python version
echo "🐍 Python version:"
poetry run python --version

echo "✅ Development environment setup complete!"
echo ""
echo "Available commands:"
echo "  poetry run python examples.py    # Run examples"
echo "  ./scripts/test.sh                # Run tests"  
echo "  ./scripts/lint.sh                # Run linters"
echo "  ./scripts/publish.sh             # Publish to PyPI"
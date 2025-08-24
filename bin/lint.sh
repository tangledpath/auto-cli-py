#!/bin/bash
# Run all linting and formatting tools

set -e

echo "🔍 Running code quality checks..."

echo "📝 Running Ruff..."
poetry run ruff check .

echo "⚫ Running Black..."
poetry run black --check .

echo "🔧 Running MyPy..."  
poetry run mypy auto_cli --ignore-missing-imports

echo "🐍 Running Pylint..."
poetry run pylint auto_cli

echo "✅ All code quality checks passed!"
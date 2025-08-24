#!/bin/bash
# Run tests with coverage

set -e

echo "🧪 Running tests with coverage..."

# Run pytest with coverage
poetry run pytest --cov=auto_cli --cov-report=term-missing --cov-report=html

echo "📊 Coverage report generated in htmlcov/"
echo "✅ Tests completed!"
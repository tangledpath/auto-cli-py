#!/bin/bash
# Build and publish package to PyPI

set -e

echo "📦 Building and publishing auto-cli-py to PyPI..."

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info/

# Build the package
echo "🔨 Building package..."
poetry build

# Show build info
echo "📋 Build information:"
ls -la dist/

# Publish to PyPI (will prompt for credentials if not configured)
echo "🚀 Publishing to PyPI..."
poetry publish

echo "✅ Published successfully to https://pypi.org/project/auto-cli-py/"
echo "📥 Install with: pip install auto-cli-py"
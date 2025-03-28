#!/usr/bin/env bash

set -e  # Exit immediately on error

# Navigate to the root of the project
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && cd .. && pwd)"
cd "$PROJECT_ROOT"

# Ensure Poetry is installed
if ! command -v poetry &> /dev/null; then
  echo "Poetry not found. Install Poetry, then try again."
  exit 1
fi

poetry install

poetry run sphinx-apidoc -f -o docs/source/_modules src

cd docs
poetry run make clean
poetry run make html

echo "✅ Docs generated at docs/build/html"

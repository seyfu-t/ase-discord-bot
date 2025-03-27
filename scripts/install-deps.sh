#!/usr/bin/env bash

# Exit on fail
set -e

# Required so that the script can be started from anywhere
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && cd .. && pwd)"

# venv path inside project folder
VENV_DIR="$PROJECT_ROOT/.venv"

# Find Python
if command -v python3 &>/dev/null; then
    PYTHON_EXEC="python3"
elif command -v python &>/dev/null; then
    PYTHON_EXEC="python"
else
    echo "Error: Python is not installed."
    exit 1
fi

# Check if venv already exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment in $VENV_DIR"
    "$PYTHON_EXEC" -m venv "$VENV_DIR"
fi

# Activate venv
source "$VENV_DIR/bin/activate"

# Install deps via poetry
cd "$PROJECT_ROOT"
poetry lock
poetry install

# Deactivate the venv
deactivate
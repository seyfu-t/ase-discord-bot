#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && cd .. && pwd)"

# Define the venv directory path (inside the project folder)
VENV_DIR="$SCRIPT_DIR/.venv"

# Find Python interpreter: prefer python3, fallback to python
if command -v python3 &>/dev/null; then
    PYTHON_EXEC="python3"
elif command -v python &>/dev/null; then
    PYTHON_EXEC="python"
else
    echo "Error: Python is not installed."
    exit 1
fi

# Check if the venv already exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment in $VENV_DIR"
    "$PYTHON_EXEC" -m venv "$VENV_DIR"
fi

# Activate the virtual environment
source "$VENV_DIR/bin/activate"

# Install dependencies using poetry (without creating another venv)
cd "$SCRIPT_DIR"
poetry install --no-root

# Deactivate the virtual environment after running
deactivate

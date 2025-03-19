#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && cd .. && pwd)"

# Activate the virtual environment
source "$SCRIPT_DIR/.venv/bin/activate"

# Run the program
python "$SCRIPT_DIR/src/main.py"

# Deactivate the virtual environment after running
deactivate
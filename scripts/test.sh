#!/usr/bin/env bash

# Exit on fail
set -e

# Required so that the script can be started from anywhere
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && cd .. && pwd)"

# Activate virtual environment
source "$PROJECT_ROOT/.venv/bin/activate"

# Run pytest on the tests folder
pytest "$PROJECT_ROOT/test"

# Deactivate virtual environment
deactivate

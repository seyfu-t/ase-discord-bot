#!/usr/bin/env bash

# Exit on fail
set -e

# Required so that the script can be started from anywhere
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && cd .. && pwd)"

# Activate venv
source "$PROJECT_ROOT/.venv/bin/activate"

# Run
python "$PROJECT_ROOT/src/ase_discord_bot/main.py"

# Deactivate venv
deactivate
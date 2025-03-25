#!/usr/bin/env bash

# Exit on fail
set -e

# Required so that the script can be started from anywhere
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && cd .. && pwd)"

# Activate venv
source "$SCRIPT_DIR/.venv/bin/activate"

# Run
python "$SCRIPT_DIR/src/ase_discord_bot/main.py"

# Deactivate venv
deactivate
# Exit immediately if a command exits with a non-zero status
set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && cd .. && pwd)"

# Build the container
docker build -f "$SCRIPT_DIR"/docker/Dockerfile -t ase-discord-bot:latest .

import os
import sys
import logging

logger = logging.getLogger(__name__)

REQUIRED_ENV_VARS = [
    "TMDB_API_KEY",
    "TMDB_READ_ACCESS_TOKEN",
    "DISCORD_TOKEN",
]

def check_env_vars():
    missing_vars = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        sys.exit(1)

class Config:
    TMDB_API_KEY = os.getenv("TMDB_API_KEY")
    TMDB_READ_ACCESS_TOKEN = os.getenv("TMDB_READ_ACCESS_TOKEN")
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
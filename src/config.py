import os
import sys
import logging

from dotenv import load_dotenv

logger = logging.getLogger(__name__)

REQUIRED_ENV_VARS = [
    "TMDB_API_KEY",
    "TMDB_READ_ACCESS_TOKEN",
    "DISCORD_TOKEN",
]


def check_env_vars():
    load_env_file()

    missing_vars = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]

    if missing_vars:
        logger.error(
            f"Missing environment variables: {', '.join(missing_vars)}")
        sys.exit(1)


def load_env_file():
    load_dotenv(".env")
    file_path = ".env.prod" if os.getenv(
        "MODE", "dev").lower() == "prod" else ".env.dev"
    load_dotenv(file_path)


class Config:
    def __init__(self):
        self.TMDB_API_KEY = str(os.getenv("TMDB_API_KEY"))
        self.TMDB_READ_ACCESS_TOKEN = str(os.getenv("TMDB_READ_ACCESS_TOKEN"))
        self.DISCORD_TOKEN = str(os.getenv("DISCORD_TOKEN"))

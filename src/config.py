import os
import sys
import logging

from dotenv import load_dotenv
from enum import Enum
from pathlib import Path

logger = logging.getLogger("Config")

ROOT_PATH = Path(__file__).resolve().parent.parent


class EnvVar(str, Enum):
    TMDB_API_KEY = "TMDB_API_KEY"
    TMDB_READ_ACCESS_TOKEN = "TMDB_READ_ACCESS_TOKEN"
    DISCORD_TOKEN = "DISCORD_TOKEN"
    DISCORD_GUILD_ID = "DISCORD_GUILD_ID"
    MODE = "MODE"


REQUIRED_ENV_VARS = [
    EnvVar.TMDB_API_KEY,
    EnvVar.TMDB_READ_ACCESS_TOKEN,
    EnvVar.DISCORD_TOKEN,
    EnvVar.DISCORD_GUILD_ID
]


def check_env_vars():
    load_env_file()

    missing_vars = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]

    if missing_vars:
        logger.error(f"Missing environment variables: {', '.join(missing_vars)}")
        sys.exit(1)

    if not str(os.getenv("DISCORD_GUILD_ID")).isdigit():
        logger.error("DISCORD_GUILD_ID must be a valid guild id")
        sys.exit(1)

    logger.info("Environment validated successfully")


def load_env_file():
    print(ROOT_PATH/".env")
    load_dotenv(ROOT_PATH / ".env")
    file_path = ROOT_PATH / (".env.prod" if os.getenv(EnvVar.MODE, "dev").lower()
                             == "prod" else ".env.dev")
    load_dotenv(file_path)


class Config:
    def __init__(self):
        self.TMDB_API_KEY = str(os.getenv(EnvVar.TMDB_API_KEY))
        self.TMDB_READ_ACCESS_TOKEN = str(os.getenv(EnvVar.TMDB_READ_ACCESS_TOKEN))
        self.DISCORD_TOKEN = str(os.getenv(EnvVar.DISCORD_TOKEN))
        self.DISCORD_GUILD_ID = int(str(os.getenv(EnvVar.DISCORD_GUILD_ID)))

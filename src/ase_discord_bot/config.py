import os
import sys
import logging
import coloredlogs

from datetime import date
from dotenv import load_dotenv
from enum import Enum
from pathlib import Path
from yarl import URL

logger = logging.getLogger("Config")

ROOT_PATH = Path(__file__).resolve().parent.parent.parent


def setup_logger():
    """
    Set up the logging configuration with colored logs.
    """
    fmt = '%(asctime)s %(levelname)-8s %(name)s %(message)s'
    coloredlogs.install(level='INFO', fmt=fmt)


class EnvVar(str, Enum):
    """
    Enum of all environment variable names.
    """
    TMDB_READ_ACCESS_TOKEN = "TMDB_READ_ACCESS_TOKEN"
    DISCORD_TOKEN = "DISCORD_TOKEN"
    DISCORD_GUILD_ID = "DISCORD_GUILD_ID"
    DISCORD_AVATAR = "DISCORD_AVATAR"
    DISCORD_BANNER = "DISCORD_BANNER"
    DISCORD_USERNAME = "DISCORD_USERNAME"
    MODE = "MODE"
    OPEN_ROUTER_API_KEY = "OPEN_ROUTER_API_KEY"
    MAX_API_PAGES_COUNT = "MAX_API_PAGES_COUNT"
    MIN_VOTE_COUNT = "MIN_VOTE_COUNT"


REQUIRED_ENV_VARS = [
    EnvVar.TMDB_READ_ACCESS_TOKEN,
    EnvVar.DISCORD_TOKEN,
    EnvVar.DISCORD_GUILD_ID,
    EnvVar.OPEN_ROUTER_API_KEY,
]


def check_and_load_env_vars():
    """
    Load and validate the presence and correctness of required environment variables.
    Logs and exits the program if any required variable is missing or invalid.
    """
    load_env_file()

    missing_vars = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]

    if missing_vars:
        logger.error(f"Missing environment variables: {', '.join(missing_vars)}")
        sys.exit(1)

    if not str(os.getenv("DISCORD_GUILD_ID")).isdigit():
        logger.error("DISCORD_GUILD_ID must be a valid guild id")
        sys.exit(1)

    if max_api := os.getenv(EnvVar.MAX_API_PAGES_COUNT):
        if not max_api.isdigit():
            logger.error(f"{EnvVar.MAX_API_PAGES_COUNT} must be an integer")
            sys.exit(1)
        if int(max_api) < 1:
            logger.error(f"{EnvVar.MAX_API_PAGES_COUNT} must be a positive integer")
            sys.exit(1)

    if min_votes := os.getenv(EnvVar.MIN_VOTE_COUNT):
        if not min_votes.isdigit():
            logger.error(f"{EnvVar.MIN_VOTE_COUNT} must be an integer")
            sys.exit(1)
        if int(min_votes) < 0:
            logger.error(f"{EnvVar.MIN_VOTE_COUNT} must be a natural number")
            sys.exit(1)

    logger.info("Environment validated successfully")


def load_env_file():
    """
    Load the appropriate environment file depending on the MODE('.env.dev' or '.env.prod').
    Always loads just '.env'.
    """
    load_dotenv(ROOT_PATH / ".env")
    file_path = ROOT_PATH / (".env.prod" if os.getenv(EnvVar.MODE, "dev").lower()
                             == "prod" else ".env.dev")
    load_dotenv(file_path)


class Config:
    """
    Load and expose configuration values from environment variables and constants.
    """

    def __init__(self):
        self.OPEN_ROUTER_API_KEY = str(os.getenv(EnvVar.OPEN_ROUTER_API_KEY))
        self.TMDB_READ_ACCESS_TOKEN = str(os.getenv(EnvVar.TMDB_READ_ACCESS_TOKEN))
        self.DISCORD_TOKEN = str(os.getenv(EnvVar.DISCORD_TOKEN))
        self.DISCORD_GUILD_ID = int(str(os.getenv(EnvVar.DISCORD_GUILD_ID)))

        self.DISCORD_AVATAR = str(os.getenv(EnvVar.DISCORD_AVATAR, ROOT_PATH / "assets/avatar.jpg"))
        self.DISCORD_BANNER = str(os.getenv(EnvVar.DISCORD_BANNER, ROOT_PATH / "assets/banner.jpg"))
        self.DISCORD_USERNAME = str(os.getenv(EnvVar.DISCORD_USERNAME, "DHBW-ASE"))
        self.MAX_API_PAGES_COUNT = int(os.getenv(EnvVar.MAX_API_PAGES_COUNT, 15))
        self.MIN_VOTE_COUNT = int(os.getenv(EnvVar.MIN_VOTE_COUNT, 100))

        self.TMDB_AUTH_HEADERS = {"Authorization": f"Bearer {self.TMDB_READ_ACCESS_TOKEN}"}
        self.TMDB_API_BASE_URL = URL("https://api.themoviedb.org/3")
        self.TMDB_IMAGES_BASE_URL = URL("https://image.tmdb.org/t/p/w500/")
        self.OPEN_ROUTER_BASE_URL = URL("https://openrouter.ai/api/v1")
        self.DISCORD_CHOICES_SIZE_LIMIT = 25
        self.ABSOLUTE_MIN_YEAR = 1874
        self.ABSOLUTE_MAX_YEAR = date.today().year

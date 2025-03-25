import os
import sys
import logging
import coloredlogs

from dotenv import load_dotenv
from enum import Enum
from pathlib import Path
from yarl import URL

logger = logging.getLogger("Config")

ROOT_PATH = Path(__file__).resolve().parent.parent.parent


def setup_logger():
    """test comment
    test
    test
    """
    fmt = '%(asctime)s %(levelname)-8s %(name)s %(message)s'
    # Root logger setup
    coloredlogs.install(level='INFO', fmt=fmt)


class EnvVar(str, Enum):
    TMDB_READ_ACCESS_TOKEN = "TMDB_READ_ACCESS_TOKEN"
    DISCORD_TOKEN = "DISCORD_TOKEN"
    DISCORD_GUILD_ID = "DISCORD_GUILD_ID"
    DISCORD_AVATAR = "DISCORD_AVATAR"
    DISCORD_BANNER = "DISCORD_BANNER"
    DISCORD_USERNAME = "DISCORD_USERNAME"
    MODE = "MODE"


REQUIRED_ENV_VARS = [
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
        self.TMDB_READ_ACCESS_TOKEN = str(os.getenv(EnvVar.TMDB_READ_ACCESS_TOKEN))
        self.DISCORD_TOKEN = str(os.getenv(EnvVar.DISCORD_TOKEN))
        self.DISCORD_GUILD_ID = int(str(os.getenv(EnvVar.DISCORD_GUILD_ID)))
        self.DISCORD_AVATAR = str(os.getenv(EnvVar.DISCORD_AVATAR, ROOT_PATH / "assets/avatar.jpg"))
        self.DISCORD_BANNER = str(os.getenv(EnvVar.DISCORD_BANNER, ROOT_PATH / "assets/banner.jpg"))
        self.DISCORD_USERNAME = str(os.getenv(EnvVar.DISCORD_USERNAME, "DHBW-ASE"))

        self.TMDB_AUTH_HEADERS = {"Authorization": f"Bearer {self.TMDB_READ_ACCESS_TOKEN}"}
        self.TMDB_API_BASE_URL = URL("https://api.themoviedb.org/3")
        self.TMDB_IMAGES_BASE_URL = URL("https://image.tmdb.org/t/p/w500/")
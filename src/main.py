from bot.discord_bot import run_bot
from config import Config, check_env_vars
from logger_config import setup_logger
import logging


setup_logger()
logger = logging.getLogger("Main")


def main():
    check_env_vars()
    cfg = Config()

    run_bot(cfg.DISCORD_TOKEN, cfg.DISCORD_GUILD_ID)


if __name__ == "__main__":
    main()

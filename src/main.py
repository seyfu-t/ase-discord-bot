from bot.discord_bot import run_bot
from config import Config, check_env_vars
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    check_env_vars()
    cfg = Config()

    logger.info("Environment validated successfully")

    run_bot(cfg.DISCORD_TOKEN)


if __name__ == "__main__":
    main()

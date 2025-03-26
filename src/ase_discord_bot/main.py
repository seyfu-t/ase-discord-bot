from ase_discord_bot.bot.discord_bot import run_bot
from ase_discord_bot.config import Config, check_env_vars, setup_logger
import logging

from ase_discord_bot.config_registry import set_config


setup_logger()
logger = logging.getLogger("Main")


def main():
    check_env_vars()
    cfg = Config()
    set_config(cfg)

    run_bot(cfg)


if __name__ == "__main__":
    main()

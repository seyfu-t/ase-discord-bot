import logging

from ase_discord_bot.bot.discord_bot import run_bot
from ase_discord_bot.config import Config, check_and_load_env_vars, setup_logger
from ase_discord_bot.config_registry import set_config


setup_logger()
logger = logging.getLogger("Main")


def main():
    """
    Main entry point for the bot.

    This function loads environment variables, creates the configuration,
    sets the global configuration, and runs the Discord bot.
    """
    check_and_load_env_vars()
    cfg = Config()
    set_config(cfg)

    run_bot()


if __name__ == "__main__":
    main()

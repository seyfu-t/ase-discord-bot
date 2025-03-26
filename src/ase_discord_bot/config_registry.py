from ase_discord_bot.config import Config


_config: Config | None = None


def set_config(config: Config):
    global _config
    _config = config


def get_config() -> Config:
    if _config is None:
        raise RuntimeError("Config has not been set.")
    return _config

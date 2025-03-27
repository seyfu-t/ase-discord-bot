from ase_discord_bot.config import Config


_config: Config | None = None


def set_config(config: Config):
    """
    Set the global configuration.

    Parameters
    ----------
    config : Config
        The configuration object to set.
    """
    global _config
    _config = config


def get_config() -> Config:
    """
    Retrieve the global configuration.

    Returns
    -------
    Config
        The current global configuration.

    Raises
    ------
    RuntimeError
        If the configuration has not been set.
    """
    if _config is None:
        raise RuntimeError("Config has not been set.")
    return _config

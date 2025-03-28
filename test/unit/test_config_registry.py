import pytest
from ase_discord_bot.config import Config
from ase_discord_bot import config_registry


@pytest.fixture(autouse=True)
def set_required_env(monkeypatch):
    monkeypatch.setenv("TMDB_READ_ACCESS_TOKEN", "dummy_tmdb")
    monkeypatch.setenv("DISCORD_TOKEN", "dummy_discord")
    monkeypatch.setenv("DISCORD_GUILD_ID", "1234")
    monkeypatch.setenv("OPEN_ROUTER_API_KEY", "dummy_open")


def test_get_config_without_setting():
    config_registry._config = None  # Reset the internal config
    with pytest.raises(RuntimeError):
        config_registry.get_config()


def test_set_and_get_config():
    conf = Config()  # This will use the environment variables set by the fixture
    config_registry.set_config(conf)
    result = config_registry.get_config()
    assert result is conf

import pytest
from ase_discord_bot.config import (
    check_and_load_env_vars,
    load_env_file,
    Config,
    setup_logger,
)
from yarl import URL

# Patch coloredlogs.install in setup_logger to prevent real logging configuration changes.


@pytest.fixture(autouse=True)
def patch_coloredlogs(monkeypatch):
    monkeypatch.setattr("ase_discord_bot.config.coloredlogs.install", lambda *args, **kwargs: None)


def test_setup_logger(monkeypatch):
    # Verify that setup_logger calls coloredlogs.install with the expected parameters.
    called = False

    def fake_install(level, fmt):
        nonlocal called
        called = True
        assert level == "INFO"
        assert fmt == '%(asctime)s %(levelname)-8s %(name)s %(message)s'
    monkeypatch.setattr("ase_discord_bot.config.coloredlogs.install", fake_install)
    setup_logger()
    assert called


def test_load_env_file(monkeypatch, tmp_path):
    # Create dummy .env files in a temporary directory.
    env_file = tmp_path / ".env"
    env_file.write_text("DUMMY=1")
    prod_file = tmp_path / ".env.prod"
    prod_file.write_text("DUMMY=prod")
    dev_file = tmp_path / ".env.dev"
    dev_file.write_text("DUMMY=dev")

    # Monkeypatch ROOT_PATH to point to tmp_path for this test.
    monkeypatch.setattr("ase_discord_bot.config.ROOT_PATH", tmp_path)

    calls = []

    def fake_load_dotenv(path):
        calls.append(str(path))
    monkeypatch.setattr("ase_discord_bot.config.load_dotenv", fake_load_dotenv)
    # Set MODE to 'prod' so that the .env.prod file is loaded.
    monkeypatch.setenv("MODE", "prod")
    load_env_file()
    assert any(".env" in call for call in calls)
    assert any(".env.prod" in call for call in calls)


def test_check_and_load_env_vars_success(monkeypatch):
    # Set all required environment variables with valid values.
    monkeyatch = monkeypatch.setenv  # shorthand
    monkeyatch("TMDB_READ_ACCESS_TOKEN", "dummy_tmdb")
    monkeyatch("DISCORD_TOKEN", "dummy_discord")
    monkeyatch("DISCORD_GUILD_ID", "1234")
    monkeyatch("OPEN_ROUTER_API_KEY", "dummy_open")
    monkeyatch("MAX_API_PAGES_COUNT", "15")
    monkeyatch("MIN_VOTE_COUNT", "100")
    # This call should not exit.
    check_and_load_env_vars()


def test_check_and_load_env_vars_missing(monkeypatch):
    # Prevent load_env_file from reloading env variables
    monkeypatch.setattr("ase_discord_bot.config.load_env_file", lambda: None)
    monkeypatch.delenv("TMDB_READ_ACCESS_TOKEN", raising=False)
    monkeypatch.setenv("DISCORD_TOKEN", "dummy_discord")
    monkeypatch.setenv("DISCORD_GUILD_ID", "1234")
    monkeypatch.setenv("OPEN_ROUTER_API_KEY", "dummy_open")
    with pytest.raises(SystemExit):
        check_and_load_env_vars()


def test_check_and_load_env_vars_invalid_guild(monkeypatch):
    # Set an invalid DISCORD_GUILD_ID.
    monkeypatch.setenv("TMDB_READ_ACCESS_TOKEN", "dummy_tmdb")
    monkeypatch.setenv("DISCORD_TOKEN", "dummy_discord")
    monkeypatch.setenv("DISCORD_GUILD_ID", "not_a_number")
    monkeypatch.setenv("OPEN_ROUTER_API_KEY", "dummy_open")
    with pytest.raises(SystemExit):
        check_and_load_env_vars()


def test_check_and_load_env_vars_invalid_max_api(monkeypatch):
    monkeypatch.setenv("TMDB_READ_ACCESS_TOKEN", "dummy_tmdb")
    monkeypatch.setenv("DISCORD_TOKEN", "dummy_discord")
    monkeypatch.setenv("DISCORD_GUILD_ID", "1234")
    monkeypatch.setenv("OPEN_ROUTER_API_KEY", "dummy_open")
    monkeypatch.setenv("MAX_API_PAGES_COUNT", "abc")  # non-digit value
    with pytest.raises(SystemExit):
        check_and_load_env_vars()


def test_check_and_load_env_vars_negative_max_api(monkeypatch):
    monkeypatch.setenv("TMDB_READ_ACCESS_TOKEN", "dummy_tmdb")
    monkeypatch.setenv("DISCORD_TOKEN", "dummy_discord")
    monkeypatch.setenv("DISCORD_GUILD_ID", "1234")
    monkeypatch.setenv("OPEN_ROUTER_API_KEY", "dummy_open")
    monkeypatch.setenv("MAX_API_PAGES_COUNT", "0")  # less than 1
    with pytest.raises(SystemExit):
        check_and_load_env_vars()


def test_check_and_load_env_vars_invalid_min_vote(monkeypatch):
    monkeypatch.setenv("TMDB_READ_ACCESS_TOKEN", "dummy_tmdb")
    monkeypatch.setenv("DISCORD_TOKEN", "dummy_discord")
    monkeypatch.setenv("DISCORD_GUILD_ID", "1234")
    monkeypatch.setenv("OPEN_ROUTER_API_KEY", "dummy_open")
    monkeypatch.setenv("MIN_VOTE_COUNT", "abc")
    with pytest.raises(SystemExit):
        check_and_load_env_vars()


def test_check_and_load_env_vars_negative_min_vote(monkeypatch):
    monkeypatch.setenv("TMDB_READ_ACCESS_TOKEN", "dummy_tmdb")
    monkeypatch.setenv("DISCORD_TOKEN", "dummy_discord")
    monkeypatch.setenv("DISCORD_GUILD_ID", "1234")
    monkeypatch.setenv("OPEN_ROUTER_API_KEY", "dummy_open")
    monkeypatch.setenv("MIN_VOTE_COUNT", "-1")
    with pytest.raises(SystemExit):
        check_and_load_env_vars()


def test_config_initialization(monkeypatch):
    # Set all required environment variables for a proper Config instance.
    monkeypatch.setenv("TMDB_READ_ACCESS_TOKEN", "dummy_tmdb")
    monkeypatch.setenv("DISCORD_TOKEN", "dummy_discord")
    monkeypatch.setenv("DISCORD_GUILD_ID", "1234")
    monkeypatch.setenv("OPEN_ROUTER_API_KEY", "dummy_open")
    monkeypatch.setenv("DISCORD_AVATAR", "avatar_path")
    monkeypatch.setenv("DISCORD_BANNER", "banner_path")
    monkeypatch.setenv("DISCORD_USERNAME", "TestUser")
    monkeypatch.setenv("MAX_API_PAGES_COUNT", "15")
    monkeypatch.setenv("MIN_VOTE_COUNT", "100")
    conf = Config()
    assert conf.TMDB_READ_ACCESS_TOKEN == "dummy_tmdb"
    assert conf.DISCORD_TOKEN == "dummy_discord"
    assert conf.DISCORD_GUILD_ID == 1234
    assert conf.OPEN_ROUTER_API_KEY == "dummy_open"
    assert conf.DISCORD_AVATAR == "avatar_path"
    assert conf.DISCORD_BANNER == "banner_path"
    assert conf.DISCORD_USERNAME == "TestUser"
    assert conf.MAX_API_PAGES_COUNT == 15
    assert conf.MIN_VOTE_COUNT == 100
    # Also check that URLs are properly constructed.
    assert conf.TMDB_API_BASE_URL == URL("https://api.themoviedb.org/3")

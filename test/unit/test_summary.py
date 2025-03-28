import pytest
from ase_discord_bot import config_registry
from ase_discord_bot.ai import summary
from ase_discord_bot.api_util.model.responses import Movie, TVShow
from ase_discord_bot.config import Config


@pytest.fixture(autouse=True)
def set_required_env(monkeypatch):
    monkeypatch.setenv("TMDB_READ_ACCESS_TOKEN", "dummy_tmdb")
    monkeypatch.setenv("DISCORD_TOKEN", "dummy_discord")
    monkeypatch.setenv("DISCORD_GUILD_ID", "1234")
    monkeypatch.setenv("OPEN_ROUTER_API_KEY", "dummy_open")
    monkeypatch.setenv("MAX_API_PAGES_COUNT", "15")
    monkeypatch.setenv("MIN_VOTE_COUNT", "100")


@pytest.fixture
def config_instance():
    conf = Config()
    config_registry.set_config(conf)
    return conf


@pytest.fixture
def dummy_movie():
    return Movie(
        adult=False,
        backdrop_path="path/to/backdrop",
        genre_ids=[1, 2],
        id=1,
        original_language="en",
        overview="Original overview",
        popularity=1.0,
        poster_path="path/to/poster",
        vote_average=8.0,
        vote_count=100,
        original_title="Original Title",
        release_date="2020-01-01",
        title="Test Movie",
        video=False,
    )


def test_get_text_movie(dummy_movie):
    text = summary._get_text(dummy_movie)
    assert "movie" in text
    assert "Title: Test Movie" in text
    assert "Summary: Original overview" in text


@pytest.fixture
def dummy_tvshow():
    return TVShow(
        adult=False,
        backdrop_path="path/to/backdrop",
        genre_ids=[3, 4],
        id=2,
        original_language="en",
        overview="TV show overview",
        popularity=2.0,
        poster_path="path/to/poster",
        vote_average=7.5,
        vote_count=150,
        origin_country=["US"],
        original_name="Original TV",
        first_air_date="2021-01-01",
        name="Test TVShow",
    )


def test_get_text_tvshow(dummy_tvshow):
    text = summary._get_text(dummy_tvshow)
    assert "tvshow" in text
    assert "Title: Test TVShow" in text
    assert "Summary: TV show overview" in text

# Dummy classes to simulate a successful API response


class DummyMessage:
    def __init__(self, content):
        self.content = content


class DummyChoice:
    def __init__(self, message):
        self.message = message


class DummyCompletion:
    choices = [DummyChoice(DummyMessage("Fake summary."))]


class DummyCompletions:
    def create(self, **kwargs):
        return DummyCompletion()


class DummyChat:
    @property
    def completions(self):
        return DummyCompletions()


class DummyOpenAI:
    def __init__(self, **kwargs):
        pass

    @property
    def chat(self):
        return DummyChat()


def test_summarize_success(monkeypatch, dummy_movie, config_instance):
    # Replace OpenAI with DummyOpenAI so that the API call returns a fake summary.
    monkeypatch.setattr(summary, "OpenAI", lambda **kwargs: DummyOpenAI())
    result = summary.summarize(dummy_movie)
    assert result == "Fake summary."

# Dummy classes to simulate a failed API call that triggers the fallback


class DummyFailureMessage:
    @property
    def content(self):
        raise TypeError("Simulated failure")


class DummyFailureChoice:
    message = DummyFailureMessage()


class DummyFailureCompletion:
    choices = [DummyFailureChoice()]


class DummyFailureCompletions:
    def create(self, **kwargs):
        return DummyFailureCompletion()


class DummyFailureChat:
    @property
    def completions(self):
        return DummyFailureCompletions()


class DummyFailureOpenAI:
    def __init__(self, **kwargs):
        pass

    @property
    def chat(self):
        return DummyFailureChat()


def test_summarize_failure(monkeypatch, dummy_movie, config_instance):
    # Replace OpenAI with DummyFailureOpenAI to simulate an API failure.
    monkeypatch.setattr(summary, "OpenAI", lambda **kwargs: DummyFailureOpenAI())
    result = summary.summarize(dummy_movie)
    # On failure, the original overview should be returned.
    assert result == dummy_movie.overview

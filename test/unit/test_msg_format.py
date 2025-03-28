import pytest
from datetime import date
from ase_discord_bot.bot import msg_format
from ase_discord_bot.api_util.model.responses import Movie

# Create a dummy Movie instance


@pytest.fixture
def dummy_movie():
    return Movie(
        adult=False,
        backdrop_path="dummy_backdrop",
        genre_ids=[1, 2],
        id=1,
        original_language="en",
        overview="A dummy overview",
        popularity=10.0,
        poster_path="/dummy.jpg",
        vote_average=8.0,
        vote_count=100,
        original_title="Original Dummy",
        release_date="2020-01-01",
        title="Dummy Movie",
        video=False,
    )


def dummy_summarize(media):
    return "Dummy summary"


def dummy_get_poster_url(poster_path):
    return f"http://dummy.url{poster_path}"


def test_help_command():
    help_text = msg_format.help_command()
    assert "Recommendation Bot Help" in help_text
    assert "/help" in help_text


def test_format_recommendation_single(monkeypatch, dummy_movie):
    # Override dependencies in _format_recommendation.
    monkeypatch.setattr(msg_format, "summarize", dummy_summarize)
    # Replace api_calls.get_poster_url with our dummy function.
    dummy_api_calls = type("DummyApiCalls", (), {"get_poster_url": dummy_get_poster_url})
    monkeypatch.setattr(msg_format, "api_calls", dummy_api_calls)

    formatted = msg_format._format_recommendation(dummy_movie)
    # Check that the formatted string contains expected pieces.
    assert "Dummy Movie" in formatted
    # The title and original title may be formatted differently if they're the same,
    # so check for the presence of either.
    assert "Original Dummy" in formatted or "-# _Original Dummy_" in formatted
    # Verify date formatting.
    assert date.fromisoformat(dummy_movie.release_date).strftime("%d.%m.%Y") in formatted
    assert "Dummy summary" in formatted


def test_format_recommendation_list(monkeypatch, dummy_movie):
    # Override dependencies as above.
    monkeypatch.setattr(msg_format, "summarize", dummy_summarize)
    dummy_api_calls = type("DummyApiCalls", (), {"get_poster_url": dummy_get_poster_url})
    monkeypatch.setattr(msg_format, "api_calls", dummy_api_calls)

    # Test with a list that has fewer than 3 items.
    results = [dummy_movie]
    formatted_list = msg_format.format_recommendation(results)
    assert len(formatted_list) == 1

    # Test with a list that has more than 3 items.
    movies = [dummy_movie for _ in range(5)]
    # Patch random.sample to return the first 3 elements.
    def monkeyatch_sample(x, k): return x[:k]
    monkeypatch.setattr(msg_format.random, "sample", monkeyatch_sample)
    formatted_list = msg_format.format_recommendation(movies)
    assert len(formatted_list) == 3

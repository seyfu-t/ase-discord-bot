import pytest
from ase_discord_bot.api_util.model.responses import Movie, TVShow
from ase_discord_bot.util.type_checks import is_list_of_movies, is_list_of_tvshows


@pytest.fixture
def dummy_movie_data():
    return {
        "adult": False,
        "backdrop_path": None,
        "genre_ids": [1],
        "id": 1,
        "original_language": "en",
        "overview": "A dummy movie overview",
        "popularity": 1.0,
        "poster_path": None,
        "vote_average": 7.5,
        "vote_count": 100,
        "original_title": "Dummy Movie",
        "release_date": "2020-01-01",
        "title": "Dummy Movie",
        "video": False,
    }


@pytest.fixture
def dummy_tvshow_data():
    return {
        "adult": False,
        "backdrop_path": None,
        "genre_ids": [1],
        "id": 2,
        "original_language": "en",
        "overview": "A dummy TV show overview",
        "popularity": 1.0,
        "poster_path": None,
        "vote_average": 7.5,
        "vote_count": 100,
        "origin_country": ["US"],
        "original_name": "Dummy TVShow",
        "first_air_date": "2020-01-01",
        "name": "Dummy TVShow",
    }


def test_is_list_of_movies_valid(dummy_movie_data):
    movie = Movie(**dummy_movie_data)
    assert is_list_of_movies([movie]) is True


def test_is_list_of_movies_empty():
    # Returns False for an empty list.
    assert is_list_of_movies([]) is False


def test_is_list_of_movies_invalid(dummy_movie_data, dummy_tvshow_data):
    movie = Movie(**dummy_movie_data)
    tvshow = TVShow(**dummy_tvshow_data)
    # Mixed list should return False.
    assert is_list_of_movies([movie, tvshow]) is False


def test_is_list_of_tvshows_valid(dummy_tvshow_data):
    tvshow = TVShow(**dummy_tvshow_data)
    assert is_list_of_tvshows([tvshow]) is True


def test_is_list_of_tvshows_empty():
    # Returns False for an empty list.
    assert is_list_of_tvshows([]) is False


def test_is_list_of_tvshows_invalid(dummy_tvshow_data, dummy_movie_data):
    tvshow = TVShow(**dummy_tvshow_data)
    movie = Movie(**dummy_movie_data)
    # Mixed list should return False.
    assert is_list_of_tvshows([tvshow, movie]) is False

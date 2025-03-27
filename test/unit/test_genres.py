import pytest

from ase_discord_bot.api_util.model.genres import MovieGenre, TVShowGenre


def test_movie_genre_properties():
    adventure = MovieGenre.ADVENTURE
    assert adventure.name_str == "Adventure"
    assert adventure.id == 12


def test_movie_genre_names_ids_and_dict():
    names = MovieGenre.names()
    ids = MovieGenre.ids()
    genre_dict = MovieGenre.as_dict()
    # Check that a known genre is in the list/dict
    assert "Adventure" in names
    assert 12 in ids
    assert genre_dict.get("Adventure") == 12


def test_movie_genre_from_name_and_from_id():
    # from_name should return the corresponding enum member
    assert MovieGenre.from_name("Comedy") == MovieGenre.COMEDY
    # from_name should raise ValueError if not found
    with pytest.raises(ValueError):
        MovieGenre.from_name("NonExistingGenre")
    # from_id should return the corresponding enum member
    assert MovieGenre.from_id(28) == MovieGenre.ACTION
    # from_id should raise ValueError for an unknown id
    with pytest.raises(ValueError):
        MovieGenre.from_id(999)


def test_tvshow_genre_properties():
    # Testing one property from TVShowGenre for example
    drama = TVShowGenre.DRAMA
    assert drama.name_str == "Drama"
    assert drama.id == 18

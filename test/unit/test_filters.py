from ase_discord_bot.api_util.model import filters
from ase_discord_bot.api_util.model.languages import Language


def test_movie_filter_assignment():
    lang = Language.ENGLISH
    mf = filters.MovieFilter(genre=3, year=2020, min_year=2010, max_year=2020, original_language=lang)
    assert mf.genre == 3
    assert mf.year == 2020
    assert mf.min_year == 2010
    assert mf.max_year == 2020
    assert mf.original_language == lang

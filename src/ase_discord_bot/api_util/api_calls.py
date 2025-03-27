import requests

from ase_discord_bot.api_util.model.filters import MovieFilter
from ase_discord_bot.api_util.model.responses import MovieResponse
from datetime import date

from ase_discord_bot.config_registry import get_config


def get_poster_url(path: str) -> str:
    cfg = get_config()
    return (cfg.TMDB_IMAGES_BASE_URL / path).human_repr()


def get_recommended_movie(movie_filter: MovieFilter) -> MovieResponse | int:
    response = _request_movie_recommendation(movie_filter)

    if response.status_code != 200:
        return response.status_code

    movie_data = MovieResponse(**response.json())

    return movie_data


def _request_movie_recommendation(movie_filter: MovieFilter) -> requests.Response:
    cfg = get_config()
    query_dict: dict[str, str | int] = {"with_genres": movie_filter.genre}

    if movie_filter.year:
        query_dict["primary_release_year"] = movie_filter.year

    if movie_filter.min_year:
        min_year_date = date(movie_filter.min_year, 1, 1)
        query_dict["primary_release_date.gte"] = min_year_date.strftime("%Y-%m-%d")

    if movie_filter.max_year:
        max_year_date = date(movie_filter.max_year, 12, 31)
        query_dict["primary_release_date.lte"] = max_year_date.strftime("%Y-%m-%d")

    if movie_filter.original_language:
        query_dict["with_original_language"] = movie_filter.original_language.iso_code

    query_url = (cfg.TMDB_API_BASE_URL / "discover/movie").human_repr()

    response = requests.get(url=query_url, params=query_dict, headers=cfg.TMDB_AUTH_HEADERS)

    return response

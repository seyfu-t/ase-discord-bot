import requests

from typing import Optional
from ase_discord_bot.api_util.model.languages import Language
from ase_discord_bot.api_util.model.responses import MovieResponse
from ase_discord_bot.config import Config
from datetime import date

from ase_discord_bot.config_registry import get_config


def get_poster_url(cfg: Config, path: str) -> str:
    return (cfg.TMDB_IMAGES_BASE_URL / path).human_repr()


def get_recommended_movie(
    genre: int,
    year: Optional[int],
    min_year: Optional[int],
    max_year: Optional[int],
    original_language: Optional[Language],
) -> MovieResponse | int:
    response = _request_movie_recommendation(genre, year, min_year, max_year, original_language)

    if response.status_code != 200:
        return response.status_code

    movie_data = MovieResponse(**response.json())

    return movie_data


def _request_movie_recommendation(
    genre: int,
    year: Optional[int],
    min_year: Optional[int],
    max_year: Optional[int],
    original_language: Optional[Language],
) -> requests.Response:
    cfg = get_config()
    query_dict: dict[str, str | int] = {"with_genres": genre}

    if year:
        query_dict["primary_release_year"] = year

    if min_year:
        min_year_date = date(min_year, 1, 1)
        query_dict["primary_release_date.gte"] = min_year_date.strftime("%Y-%m-%d")

    if max_year:
        max_year_date = date(max_year, 12, 31)
        query_dict["primary_release_date.lte"] = max_year_date.strftime("%Y-%m-%d")

    if original_language:
        query_dict["with_original_language"] = original_language.iso_code

    query_url = (cfg.TMDB_API_BASE_URL / "discover/movie").human_repr()

    response = requests.get(url=query_url, params=query_dict, headers=cfg.TMDB_AUTH_HEADERS)

    return response

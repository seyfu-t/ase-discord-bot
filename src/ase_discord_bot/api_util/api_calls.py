import requests

from ase_discord_bot.api_util.model.filters import MovieFilter
from ase_discord_bot.api_util.model.responses import Movie, MovieResponse
from datetime import date

from ase_discord_bot.config_registry import get_config


def get_poster_url(path: str) -> str:
    cfg = get_config()
    return (cfg.TMDB_IMAGES_BASE_URL / path).human_repr()


def get_recommended_movie(movie_filter: MovieFilter) -> list[Movie] | list[int]:
    responses = _request_movie_recommendation(movie_filter)

    error_codes: list[int] = []
    movies_data: list[Movie] = []

    for response in responses:
        if response.status_code != 200:
            error_codes.append(response.status_code)
        else:
            movie_data = MovieResponse(**response.json()).results
            movies_data.extend(movie_data)

    # If every single request failed
    if (len(error_codes) == len(responses)):
        return error_codes

    return movies_data


def _request_movie_recommendation(movie_filter: MovieFilter) -> list[requests.Response]:
    cfg = get_config()
    query_dict: dict[str, str | int] = {
        "with_genres": movie_filter.genre,
        "sort_by": "MIN_VOTE_COUNT",
        "vote_count.gte": cfg.MIN_VOTE_COUNT,
    }

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

    responses = []

    first_response = requests.get(url=query_url, params=query_dict, headers=cfg.TMDB_AUTH_HEADERS)
    responses.append(first_response)
    max_pages_count = int(responses[0].json()["total_pages"])

    for i in range(2, min(max_pages_count, cfg.MAX_API_PAGES_COUNT) + 1):
        query_dict["page"] = i
        response = requests.get(url=query_url, params=query_dict, headers=cfg.TMDB_AUTH_HEADERS)
        responses.append(response)

    return responses

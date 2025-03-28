import requests

from ase_discord_bot.api_util.model.filters import MovieFilter, TVShowFilter
from ase_discord_bot.api_util.model.responses import Movie, MovieResponse, TVShow, TVShowResponse
from datetime import date
from ase_discord_bot.config_registry import get_config


def get_poster_url(path: str) -> str:
    """
    Returns the full poster image URL for a given image path.

    Args:
        path (str): Relative path of the image from the API.

    Returns:
        str: Full URL to the image.
    """
    cfg = get_config()
    return (cfg.TMDB_IMAGES_BASE_URL / path).human_repr()


def get_recommended_movie(movie_filter: MovieFilter) -> list[Movie] | list[int]:
    """
    Retrieves recommended movies based on the given filter.

    Args:
        movie_filter (MovieFilter): Filter criteria for movie recommendations.

    Returns:
        list[Movie] | list[int]: A list of Movie objects, or HTTP error codes if all requests fail.
    """
    responses = _request_recommendation(movie_filter)

    error_codes: list[int] = []
    movies_data: list[Movie] = []

    for response in responses:
        if response.status_code != 200:
            error_codes.append(response.status_code)
        else:
            movie_data = MovieResponse(**response.json()).results
            movies_data.extend(movie_data)

    # If every single request failed
    if (len(error_codes) == len(responses) != 0):
        return error_codes

    return movies_data


def get_recommended_tvshow(tvshow_filter: TVShowFilter) -> list[TVShow] | list[int]:
    """
    Retrieves recommended TV shows based on the given filter.

    Args:
        tvshow_filter (TVShowFilter): Filter criteria for TV show recommendations.

    Returns:
        list[TVShow] | list[int]: A list of TVShow objects, or HTTP error codes if all requests fail.
    """
    responses = _request_recommendation(tvshow_filter)

    error_codes: list[int] = []
    tvshows_data: list[TVShow] = []

    for response in responses:
        if response.status_code != 200:
            error_codes.append(response.status_code)
        else:
            tvshow_data = TVShowResponse(**response.json()).results
            tvshows_data.extend(tvshow_data)

    # If every single request failed
    if (len(error_codes) == len(responses)):
        return error_codes

    return tvshows_data


def _request_recommendation(media_filter: MovieFilter | TVShowFilter) -> list[requests.Response]:
    """
    Sends paginated requests to TMDB based on the provided media filter.

    Args:
        media_filter (MovieFilter | TVShowFilter): Filter for the API request.

    Returns:
        list[requests.Response]: API responses from TMDB.
    """
    cfg = get_config()
    query_dict: dict[str, str | int] = {
        "with_genres": media_filter.genre,
        "sort_by": "vote_average.desc",
        "vote_count.gte": cfg.MIN_VOTE_COUNT,
    }

    if isinstance(media_filter, MovieFilter):
        media_type = "movie"
    elif isinstance(media_filter, TVShowFilter):
        media_type = "tv"

    if media_filter.year:
        if media_type == "movie":
            query_dict["primary_release_year"] = media_filter.year
        elif media_type == "tv":
            query_dict["first_air_date_year"] = media_filter.year

    if media_filter.min_year:
        min_year_date = date(media_filter.min_year, 1, 1)
        if media_type == "movie":
            query_dict["primary_release_date.gte"] = min_year_date.strftime("%Y-%m-%d")
        elif media_type == "tv":
            query_dict["first_air_date.gte"] = min_year_date.strftime("%Y-%m-%d")

    if media_filter.max_year:
        max_year_date = date(media_filter.max_year, 12, 31)
        if media_type == "movie":
            query_dict["primary_release_date.lte"] = max_year_date.strftime("%Y-%m-%d")
        elif media_type == "tv":
            query_dict["first_air_date.lte"] = max_year_date.strftime("%Y-%m-%d")

    if media_filter.original_language:
        query_dict["with_original_language"] = media_filter.original_language.iso_code

    query_url = (cfg.TMDB_API_BASE_URL / f"discover/{media_type}").human_repr()

    responses = []

    first_response = requests.get(url=query_url, params=query_dict, headers=cfg.TMDB_AUTH_HEADERS)
    responses.append(first_response)
    max_pages_count = int(responses[0].json()["total_pages"])

    for i in range(2, min(max_pages_count, cfg.MAX_API_PAGES_COUNT) + 1):
        query_dict["page"] = i
        response = requests.get(url=query_url, params=query_dict, headers=cfg.TMDB_AUTH_HEADERS)
        responses.append(response)

    return responses

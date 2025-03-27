import random

from datetime import date
from ase_discord_bot.ai.summary import summarize
from ase_discord_bot.api_util import api_calls
from ase_discord_bot.api_util.model.responses import Movie, MovieResponse, TVShowResponse


def format_recommendation(response: MovieResponse | TVShowResponse) -> list[str]:
    if type(response) is MovieResponse:
        formatted_responses: list[str] = []

        picked_movies = random.sample(response.results, 3)
        for movie in picked_movies:
            formatted_responses.append(_format_recommendation_movie(movie))

        return formatted_responses

    return []


def _format_recommendation_movie(movie: Movie) -> str:
    formatted_response: list[str] = []

    formatted_response.append(f"### *{movie.title}*")

    if movie.title != movie.original_title:
        formatted_response.append(f"-# _{movie.original_title}_")

    formatted_response.append(f"- Released: {date.fromisoformat(movie.release_date).strftime('%d.%m.%Y')}")

    ai_summary = summarize(movie)
    formatted_response.append(f"- Description: {ai_summary}")

    if movie.poster_path:
        poster_url = api_calls.get_poster_url(movie.poster_path[1:])
        formatted_response.append(f"![{movie.title}.jpg]({poster_url})")

    return "\n".join(formatted_response)

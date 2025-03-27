import random

from datetime import date
from ase_discord_bot.ai.summary import summarize
from ase_discord_bot.api_util import api_calls
from ase_discord_bot.api_util.model.responses import Movie, TVShow


def format_recommendation(results: list[Movie] | list[TVShow]) -> list[str]:
    formatted_responses: list[str] = []

    picked_movies = random.sample(results, 3) if len(results) >= 3 else results

    for movie in picked_movies:
        formatted_responses.append(_format_recommendation(movie))

    return formatted_responses


def _format_recommendation(media: Movie | TVShow) -> str:
    formatted_response: list[str] = []

    if isinstance(media, Movie):
        title = media.title
        original_title = media.original_title
        release_date = media.release_date
    elif isinstance(media, TVShow):
        title = media.name
        original_title = media.original_name
        release_date = media.first_air_date

    formatted_response.append(f"### 🎬 *{title}*")

    if title != original_title:
        formatted_response.append(f"-# _{original_title}_")

    formatted_response.append(f"🗓️ Released: {date.fromisoformat(release_date).strftime('%d.%m.%Y')}")

    ai_summary = summarize(media)
    formatted_response.append(f"🎞️ Description: {ai_summary}")

    if media.poster_path:
        poster_url = api_calls.get_poster_url(media.poster_path[1:])
        formatted_response.append(f"[{title}.jpg]({poster_url})")

    return "\n".join(formatted_response)

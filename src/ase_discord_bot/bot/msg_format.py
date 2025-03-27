import random

from datetime import date
from ase_discord_bot.ai.summary import summarize
from ase_discord_bot.api_util import api_calls
from ase_discord_bot.api_util.model.responses import Movie, TVShow


def format_recommendation(results: list[Movie] | list[TVShow]) -> list[str]:
    """
    Format a list of media recommendations into displayable strings.

    If there are at least three items in the results, randomly selects three to format.
    Otherwise, formats all provided items.

    Parameters
    ----------
    results : list[Movie] | list[TVShow]
        The list of movies or TV shows to format.

    Returns
    -------
    list[str]
        A list of formatted recommendation strings.
    """
    formatted_responses: list[str] = []

    picked_movies = random.sample(results, 3) if len(results) >= 3 else results

    for movie in picked_movies:
        formatted_responses.append(_format_recommendation(movie))

    return formatted_responses


def _format_recommendation(media: Movie | TVShow) -> str:
    """
    Format a single media item into a recommendation string.

    Includes the title, release date, a summarized description,
    and a poster URL if available.

    Parameters
    ----------
    media : Movie | TVShow
        The media item (movie or TV show) to format.

    Returns
    -------
    str
        A formatted recommendation string.
    """
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


def help_command() -> str:
    """
    Generate the help message for the recommendation bot.

    Returns
    -------
    str
        A string containing the help message for available commands.
    """
    return (
        "**Recommendation Bot Help**\n\n"
        "Welcome! Use the commands below to get movie and TV show recommendations.\n\n"
        "🔹 **/recommend_movie**\n"
        "   - **Description:** Get a movie recommendation based on genre, release year, and language.\n"
        "   - **Parameters:**\n"
        "       • `genre` (required): Choose a movie genre.\n"
        "       • `year` (optional): Specify a release year.\n"
        "       • `min_year` and `max_year` (optional): Define a range for the release year.\n"
        "       • `original_language` (optional): Specify the movie's original language.\n\n"
        "🔹 **/recommend_tvshow**\n"
        "   - **Description:** Get a TV show recommendation based on genre, release year, and language.\n"
        "   - **Parameters:**\n"
        "       • `genre` (required): Choose a TV show genre.\n"
        "       • `year` (optional): Specify a release year.\n"
        "       • `min_year` and `max_year` (optional): Define a range for the release year.\n"
        "       • `original_language` (optional): Specify the TV show's original language.\n\n"
        "🔹 **/help**\n"
        "   - **Description:** Displays this help message."
    )

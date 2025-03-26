from datetime import date
from ase_discord_bot.ai.summary import summarize
from ase_discord_bot.api_util.model.responses import Movie, MovieResponse, TVShowResponse


def format_recommendation(response: MovieResponse | TVShowResponse):
    if type(response) is MovieResponse:
        formatted_response: str = ""

        # for movie in response.results:
        movie = response.results[0]
        formatted_response += _format_recommendation_movie(movie)
        formatted_response += "\n"

        return formatted_response


def _format_recommendation_movie(movie: Movie) -> str:
    formatted_response: list[str] = []

    formatted_response.append(f"### *{movie.title}*")

    if movie.title != movie.original_title:
        formatted_response.append(f"-# _{movie.original_title}_")

    formatted_response.append(f"- Released: {date.fromisoformat(movie.release_date).strftime('%d.%sm.%Y')}")

    ai_summary = summarize(movie)
    formatted_response.append(f"- Description: {ai_summary}")

    # if movie.poster_path:
    #     poster_url = api_calls.get_poster_url(cfg, movie.poster_path[1:])
    #     formatted_response.append(f"![{movie.title}.jpg]({poster_url})")

    return "\n".join(formatted_response)

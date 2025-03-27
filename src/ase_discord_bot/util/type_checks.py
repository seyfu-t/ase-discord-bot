from typing import Any, TypeGuard
from ase_discord_bot.api_util.model.responses import Movie, TVShow


def is_list_of_movies(lst: list[Any]) -> TypeGuard[list[Movie]]:
    return bool(lst) and all(isinstance(x, Movie) for x in lst)


def is_list_of_tvshows(lst: list[Any]) -> TypeGuard[list[TVShow]]:
    return bool(lst) and all(isinstance(x, TVShow) for x in lst)

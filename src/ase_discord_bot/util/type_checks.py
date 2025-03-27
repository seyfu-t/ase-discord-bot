from typing import Any, TypeGuard
from ase_discord_bot.api_util.model.responses import Movie, TVShow


def is_list_of_movies(lst: list[Any]) -> TypeGuard[list[Movie]]:
    """
    Check if the list contains only Movie instances.

    Parameters
    ----------
    lst : list[Any]
        The list to check.

    Returns
    -------
    TypeGuard[list[Movie]]
        True if all elements in the list are instances of Movie, otherwise False.
    """
    return bool(lst) and all(isinstance(x, Movie) for x in lst)


def is_list_of_tvshows(lst: list[Any]) -> TypeGuard[list[TVShow]]:
    """
    Check if the list contains only TVShow instances.

    Parameters
    ----------
    lst : list[Any]
        The list to check.

    Returns
    -------
    TypeGuard[list[TVShow]]
        True if all elements in the list are instances of TVShow, otherwise False.
    """
    return bool(lst) and all(isinstance(x, TVShow) for x in lst)

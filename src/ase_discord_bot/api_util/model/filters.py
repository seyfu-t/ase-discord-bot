from dataclasses import dataclass
from typing import Optional
from ase_discord_bot.api_util.model.languages import Language


@dataclass
class MovieFilter:
    """
    Filter criteria for movie recommendations.

    Attributes
    ----------
    genre : int
        The movie genre ID.
    year : Optional[int]
        Specific release year.
    min_year : Optional[int]
        Minimum release year.
    max_year : Optional[int]
        Maximum release year.
    original_language : Optional[Language]
        The original language filter.
    """
    genre: int
    year: Optional[int] = None
    min_year: Optional[int] = None
    max_year: Optional[int] = None
    original_language: Optional[Language] = None


@dataclass
class TVShowFilter:
    """
    Filter criteria for TV show recommendations.

    Attributes
    ----------
    genre : int
        The TV show genre ID.
    year : Optional[int]
        Specific release year.
    min_year : Optional[int]
        Minimum release year.
    max_year : Optional[int]
        Maximum release year.
    original_language : Optional[Language]
        The original language filter.
    """
    genre: int
    year: Optional[int] = None
    min_year: Optional[int] = None
    max_year: Optional[int] = None
    original_language: Optional[Language] = None

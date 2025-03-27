from dataclasses import dataclass
from typing import Optional

from ase_discord_bot.api_util.model.languages import Language


@dataclass
class MovieFilter:
    genre: int
    year: Optional[int] = None
    min_year: Optional[int] = None
    max_year: Optional[int] = None
    original_language: Optional[Language] = None


@dataclass
class TVShowFilter:
    genre: int
    year: Optional[int] = None
    min_year: Optional[int] = None
    max_year: Optional[int] = None
    original_language: Optional[Language] = None

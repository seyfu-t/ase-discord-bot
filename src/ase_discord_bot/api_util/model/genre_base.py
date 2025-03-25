from enum import Enum
from typing import Self
from discord import OptionChoice


class GenreEnum(Enum):
    @property
    def name_str(self) -> str:
        return self.value[0]

    @property
    def id(self) -> int:
        return self.value[1]

    @classmethod
    def names(cls) -> list[str]:
        return [genre.name_str for genre in cls]

    @classmethod
    def ids(cls) -> list[int]:
        return [genre.id for genre in cls]

    @classmethod
    def as_dict(cls) -> dict[str, int]:
        return {genre.name_str: genre.id for genre in cls}

    @classmethod
    def as_choices(cls) -> list[OptionChoice]:
        return [OptionChoice(name=genre.name_str, value=genre.id) for genre in cls]

    @classmethod
    def from_name(cls, name: str) -> Self:
        for genre in cls:
            if genre.name_str == name:
                return genre
        raise ValueError(f"No genre with name '{name}' found in {cls.__name__}")

    @classmethod
    def from_id(cls, genre_id: int) -> Self:
        for genre in cls:
            if genre.id == genre_id:
                return genre
        raise ValueError(f"No genre with id '{genre_id}' found in {cls.__name__}")

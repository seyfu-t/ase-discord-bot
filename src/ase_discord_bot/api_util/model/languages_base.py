from enum import Enum
from typing import Optional, Self
from difflib import SequenceMatcher


class LanguageEnum(Enum):
    @property
    def iso_code(self) -> str:
        return self.value[0]

    @property
    def english_name(self) -> str:
        return self.value[1]

    @property
    def local_name(self) -> str | None:
        return self.value[2]

    @classmethod
    def all_iso_codes(cls):
        return [lang.iso_code for lang in cls]

    @classmethod
    def all_english_names(cls) -> list[str]:
        return [lang.english_name for lang in cls]

    @classmethod
    def all_local_names(cls):
        return [lang.local_name for lang in cls]

    @classmethod
    def all_names(cls) -> list[str]:
        return [(lang.local_name if lang.local_name else lang.english_name) for lang in cls]

    @classmethod
    def from_iso_code(cls, code: str):
        for lang in cls:
            if lang.iso_code == code:
                return lang
        raise ValueError(f"No language with ISO code '{code}' found in {cls.__name__}")

    @classmethod
    def from_english_name(cls, name: str):
        for lang in cls:
            if lang.english_name == name:
                return lang
        raise ValueError(f"No language with English name '{name}' found in {cls.__name__}")

    @classmethod
    def from_fuzzy(cls, query: Optional[str]) -> Optional[Self]:
        if query is None:
            return None
        query = query.strip().lower()
        best_match = None
        best_score = 0

        for lang in cls:
            candidates = [
                lang.iso_code.lower(),
                lang.english_name.lower(),
            ]
            if lang.local_name:
                candidates.append(lang.local_name.lower())

            for candidate in candidates:
                if query == candidate:
                    return lang

                if query in candidate:
                    score = len(query) / len(candidate)
                else:
                    score = SequenceMatcher(None, query, candidate).ratio()

                if score > best_score:
                    best_score = score
                    best_match = lang

        if best_score > 0.6:
            return best_match
        else:
            return None

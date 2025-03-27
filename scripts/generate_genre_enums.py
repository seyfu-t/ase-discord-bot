#!/usr/bin/env python
import json
from pathlib import Path


def format_enum_name(name):
    key = name.upper()
    key = key.replace(" & ", "_AND_").replace(" ", "_").replace("-", "_")

    return key


def generate_genres_enums(movie_json, tvshow_json):
    file_lines = []
    movie_lines = []
    tvshow_lines = []

    # Sort by id ascending
    movie_data = sorted(movie_json["genres"], key=lambda x: x["id"])
    tvshow_data = sorted(tvshow_json["genres"], key=lambda x: x["id"])

    # Convert each entry into a single line of an enum
    for genre in movie_data:
        genre_id = genre["id"]
        name = genre["name"]
        enum_name = format_enum_name(name)

        movie_lines.append(f"    {enum_name} = (\"{name}\", {genre_id})")

    for genre in tvshow_data:
        genre_id = genre["id"]
        name = genre["name"]
        enum_name = format_enum_name(name)

        tvshow_lines.append(f"    {enum_name} = (\"{name}\", {genre_id})")

    # Assemble file
    file_lines = "from ase_discord_bot.api_util.model.genre_base import GenreEnum\n"
    file_lines += "\n"
    file_lines += "\n"
    file_lines += "class MovieGenre(GenreEnum):\n"
    file_lines += "\n".join(movie_lines)
    file_lines += "\n"
    file_lines += "\n"
    file_lines += "class TVShowGenre(GenreEnum):\n"
    file_lines += "\n".join(tvshow_lines)

    return file_lines


if __name__ == "__main__":
    PROJECT_ROOT_PATH = Path(__file__).resolve().parent.parent

    with open(PROJECT_ROOT_PATH / "assets/movie_genres.json", "r", encoding="utf-8") as movie_file:
        movie_json = json.load(movie_file)
    with open(PROJECT_ROOT_PATH / "assets/tvshow_genres.json", "r", encoding="utf-8") as tvshow_file:
        tvshow_json = json.load(tvshow_file)

    enum_str = generate_genres_enums(movie_json, tvshow_json)

    with open(PROJECT_ROOT_PATH / "src/ase_discord_bot/api_util/model/genres.py", "w", encoding="utf-8") as f:
        f.write(enum_str)

    print("Genres enum file successfully generated.")

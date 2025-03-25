#!/usr/bin/env python
import json
from pathlib import Path


def format_enum_name(english_name) -> str:
    key = english_name.upper().replace(" ", "_").replace(";", "")
    key = key.replace(",", "").replace("-", "_").replace("/", "_")

    key = ''.join(c if c.isalnum() or c == '_' else '' for c in key)
    if key[0].isdigit():
        key = f"LANG_{key}"
    return key


def generate_language_enum(json_data: list[dict], class_name="Language", enum_name="LanguageEnum") -> str:
    enum_lines = []
    keys = []

    json_data = sorted(json_data, key=lambda x: x["iso_639_1"])

    for entry in json_data:
        iso = entry["iso_639_1"]
        english_name = entry["english_name"]
        local_name = entry["name"].strip() or None

        key = format_enum_name(english_name)

        if key in keys:
            continue
        keys.append(key)
        enum_lines.append(f'    {key} = ("{iso}", "{english_name}", {repr(local_name)})')

    enum_code = f"from ase_discord_bot.api_util.model.languages_base import {enum_name}\n"
    enum_code += "\n"
    enum_code += "\n"
    enum_code += f"class {class_name}({enum_name}):\n"
    enum_code += "\n".join(enum_lines)
    enum_code += "\n"

    return enum_code


if __name__ == '__main__':
    PROJECT_ROOT_PATH = Path(__file__).resolve().parent.parent
    with open(PROJECT_ROOT_PATH / "assets/languages.json", "r", encoding="utf-8") as f:
        language_data = json.load(f)

    enum_str = generate_language_enum(language_data)

    with open(PROJECT_ROOT_PATH / "src/ase_discord_bot/api_util/model/languages.py", "w", encoding="utf-8") as f:
        f.write(enum_str)

    print("Languages enum file successfully generated")

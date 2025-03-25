import requests
from ase_discord_bot.api_util.model.languages import Language
from ase_discord_bot.config import check_env_vars, Config


def normalize_language_entry(entry):
    iso = entry["iso_639_1"]
    english_name = entry["english_name"]
    local_name = entry["name"].strip() or None

    key = english_name.upper().replace(" ", "_").replace(";", "").replace(",", "").replace("-", "_").replace("/", "_")
    key = ''.join(c if c.isalnum() or c == '_' else '' for c in key)
    if key[0].isdigit():
        key = f"LANG_{key}"

    return key, (iso, english_name, local_name)


def test_enum_matches_tmdb_api():
    check_env_vars()
    cfg = Config()
    # should be mocked ideally, but using actual api for now
    url = (cfg.TMDB_API_BASE_URL / "configuration/languages").human_repr()
    response = requests.get(url, headers=cfg.TMDB_AUTH_HEADERS)
    assert response.status_code == 200

    api_data = sorted(response.json(), key=lambda x: x["iso_639_1"])

    keys = []

    # Removing duplicates
    for entry in api_data:
        english_name = entry["english_name"]

        key = english_name.upper().replace(" ", "_").replace(";", "")
        key = key.replace(",", "").replace("-", "_").replace("/", "_")

        key = ''.join(c if c.isalnum() or c == '_' else '' for c in key)
        if key[0].isdigit():
            key = f"LANG_{key}"

        if key in keys:
            api_data.remove(entry)
            continue
        keys.append(key)

    expected = dict(normalize_language_entry(e) for e in api_data)
    actual = {member.name: (member.value[0], member.english_name, member.local_name) for member in Language}

    assert expected == actual

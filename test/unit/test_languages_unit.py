import pytest

from ase_discord_bot.api_util.model.languages import Language


def test_language_properties():
    english = Language.ENGLISH
    assert english.iso_code == "en"
    assert english.english_name == "English"
    # The local_name for English is set to 'English' in your definition.
    assert english.local_name == "English"


def test_all_iso_codes():
    codes = Language.all_iso_codes()
    # Check that some known ISO codes exist
    assert "en" in codes
    assert "fr" in codes


def test_from_iso_code_and_from_english_name():
    # from_iso_code should return the correct enum member
    assert Language.from_iso_code("fr") == Language.FRENCH
    with pytest.raises(ValueError):
        Language.from_iso_code("xx_wrong")
    # from_english_name should return the correct member
    assert Language.from_english_name("German") == Language.GERMAN
    with pytest.raises(ValueError):
        Language.from_english_name("NonExistentLanguage")


def test_from_fuzzy_exact_match():
    # An exact query should immediately match
    assert Language.from_fuzzy("english") == Language.ENGLISH


def test_from_fuzzy_partial_match():
    # A partial query should return the closest match if above threshold
    lang = Language.from_fuzzy("germ")
    assert lang == Language.GERMAN


def test_from_fuzzy_no_match():
    # A query that doesn't meet the threshold should return None
    assert Language.from_fuzzy("zzzzz") is None

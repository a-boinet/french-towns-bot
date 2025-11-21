import pytest

from src.config import Config
from src.validator import is_valid


NAMES_TO_TEST = [
    ("", False),  # Too short
    ("V" * max(0, Config.MIN_CITY_LENGTH - 1), False),  # Too short
    ("V" * Config.MIN_CITY_LENGTH, True),
    ("V" * Config.MAX_WORD_LENGTH, True),
    ("V" * (Config.MAX_WORD_LENGTH + 1), False),  # Too long
    ("V" * Config.MAX_WORD_LENGTH + "-" + "V" * Config.MAX_WORD_LENGTH, True),
    ("V" * Config.MAX_WORD_LENGTH + " " + "V" * Config.MAX_WORD_LENGTH, True),
    ("-V", False),  # Starts with a dash
    ("V-", False),  # Ends with a dash
    ("Ville-sur-sur-mer", False),  # Double "-sur-"
    ("Ville-sur-mer", True),
    ("l'Adresse-sur-Mer", True),
    ("Shit", False),  # Forbidden word
    ("Fromage", False),  # French word
]


@pytest.mark.parametrize(
    "name, name_is_valid",
    NAMES_TO_TEST,
    ids=[v[0] for v in NAMES_TO_TEST],
)
def test_string_reformating(name, name_is_valid):
    assert (
        is_valid(name) == name_is_valid
    ), f"The name {name} is actually {'valid' if is_valid(name) else 'invalid'}!"

from pathlib import Path

from src.config import Config


def load_words_from_file(file_path: Path) -> set[str]:
    with open(file_path, "r") as f:
        words = {word.strip().lower() for word in f.readlines()}
    return words


FORBIDDEN_WORDS = load_words_from_file(Config.RESOURCES_DIR / "forbidden_words.txt")
FORBIDDEN_PATTERNS = load_words_from_file(
    Config.RESOURCES_DIR / "forbidden_patterns.txt"
)
FRENCH_DICTIONARY = load_words_from_file(Config.RESOURCES_DIR / "french_dictionary.txt")
try:
    ALREADY_TWEETED = load_words_from_file(Config.CACHE_DIR / "already_tweeted.txt")
except FileNotFoundError:
    ALREADY_TWEETED: set[str] = set()


def is_valid(name: str) -> bool:
    """
    Try to find out if `name` sounds french or not
    :param name: The name we want to validate
    :returns: True or False
    """
    name_lower = name.lower()

    if (  # Quick checks for starters
        len(name_lower) < Config.MIN_CITY_LENGTH  # Too short
        or len(name_lower) > Config.MAX_CITY_LENGTH  # Too long
        or name_lower.startswith("x")  # Doesn't sound french
        or name_lower.count("-") >= 5  # To many words
    ):
        return False

    # Long words inside name
    for chunk in name_lower.split("-"):
        if len(chunk) > Config.MAX_WORD_LENGTH:
            # Contains a long word
            return False

    # Forbidden words, French words and names already tweeted
    for words in [FORBIDDEN_WORDS, FRENCH_DICTIONARY, ALREADY_TWEETED]:
        if name_lower in words:
            return False

    # Forbidden patterns
    pattern_word = " " + name_lower + " "
    for fp in FORBIDDEN_PATTERNS:
        if fp in pattern_word:
            # Contains a forbidden pattern
            return False

    return True


def save_city_name(city_name: str):
    try:
        with open(Config.CACHE_DIR / "already_tweeted.txt", "a") as f:
            f.write(f"{city_name}\n")
    except IOError:
        print(f"Couldn't save name '{city_name}' to `already_tweeted.txt`")

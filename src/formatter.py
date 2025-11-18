import re

from src.config import Config


with open(Config.RESOURCES_DIR / "replace_patterns.txt", "r") as f:
    REPLACE_PATTERNS: list[list[str]] = [
        pattern.strip().split(",") for pattern in f.readlines()
    ]


def intersperse(lst, item):
    """
    Adapted from Stack Overflow
    https://stackoverflow.com/a/6300649/
    """
    result = [item] * (2 * len(lst) - 1)
    result[::2] = lst
    return result


def reformat_name(name: str):
    """
    Takes a string like "L'aDResse-SuR-sur-MeR"
    and returns "l'Adresse-sur-Mer"
    """
    # Removing whitespaces
    name = name.strip()

    # Split using "-"
    words_1 = name.lower().split("-")
    words_1 = intersperse(words_1, "-")

    # Split using "'"
    words_2 = []
    for element in words_1:
        words_2.extend(intersperse(element.split("'"), "'"))

    # Split using '"'
    words_3 = []
    for element in words_2:
        words_3.extend(intersperse(element.split(" "), " "))

    # Compile the final string, with each "word" capitalized
    final_name = ""
    for word in words_3:
        final_name += word.capitalize()

    # Delete repeating patterns
    # (longer than two letters, to preserve double letters in words)
    final_name = re.sub(r"(.{2,}?)\1+", r"\1", final_name)

    # Replace some common patterns
    for pattern in REPLACE_PATTERNS:
        final_name = final_name.replace(pattern[0], pattern[1])

    # We have the final string!
    return final_name

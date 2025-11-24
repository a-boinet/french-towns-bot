import pytest

from src.formatter import reformat_name


PAIR_TO_TEST = [
    ("l'aDResse-SuR-MeR", "l'Adresse-sur-Mer"),
    ("saint-martin", "Saint-Martin"),
    ("Ville-sur-SuR-sUr-sur-Sur-seine", "Ville-sur-Seine"),
]


@pytest.mark.parametrize(
    "initial_name, target_name",
    PAIR_TO_TEST,
    ids=[pair[1] for pair in PAIR_TO_TEST],
)
def test_string_reformating(initial_name, target_name):
    name_reformated = reformat_name(initial_name)
    # Check if we got the target name
    assert name_reformated == target_name
    # Check if `reformat_name` is idempotent
    assert reformat_name(name_reformated) == target_name

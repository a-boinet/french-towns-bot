from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    BASE_DIR: Path = Path(__file__).parent.parent
    RESOURCES_DIR: Path = BASE_DIR / "resources"
    CACHE_DIR: Path = RESOURCES_DIR / "cache"
    CONTEXT_LENGTH: int = 4
    MIN_CITY_COUNT_PER_REGION: int = 300
    # The population is generated using an exponential distribution (~0.0009 for France)
    POPULATION_LAMBDA: float = 0.0009
    MIN_CITY_LENGTH: int = 4
    MAX_CITY_LENGTH: int = 30
    MAX_WORD_LENGTH: int = 14
    MAX_WORD_COUNT: int = 5
    MAX_REPLACE_ATTEMPT: int = 20
    WAIT_TIME_BEFORE_RETRY: int = 1800  # 1800 sec -> 30 min

    def __post_init__(self):  # NOQA
        assert (
            Config.CONTEXT_LENGTH >= 2
        ), f"Context length must be at least 2 (current value: {Config.CONTEXT_LENGTH})"

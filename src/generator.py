import os
import random as rd
from collections import deque

from emoji import emojize

from src.config import Config
from src.cache_files_utils import (
    MAIN_CACHE_FILE_PATH,
    generate_all_cache_files,
    read_data_from_file,
    get_cache_file_path_from_region_name,
)
from src.formatter import reformat_name
from src.validator import is_valid


def get_random_region() -> dict:
    if not os.path.exists(MAIN_CACHE_FILE_PATH):
        print("Cache files missing!")
        # We don't have the required cache files - Let's generate them!
        generate_all_cache_files()

    # Load the main cache file
    cache_data = read_data_from_file(MAIN_CACHE_FILE_PATH, data_is_compressed=False)
    cities_count_by_region: dict[str, int] = {
        region: city_count
        for region, city_count in cache_data["cities_count_by_region"].items()
        # Some regions are not used because the lack of
        # training material yields poor result
        if city_count > Config.MIN_CITY_COUNT_PER_REGION
    }

    # Then, pick a region
    region_name: str = rd.choices(
        population=list(cities_count_by_region.keys()),
        weights=list(cities_count_by_region.values()),
        k=1,  # Only need one choice
    )[0]

    # Load the cache for the region we picked
    region_cache = read_data_from_file(
        get_cache_file_path_from_region_name(region_name), data_is_compressed=True
    )
    return region_cache


def generate_new_city_name():
    continue_generation = True
    while continue_generation:
        region_cache = get_random_region()
        cities_count_by_name_length = region_cache["cities_count_by_name_length"]
        distribution_dict = region_cache["distribution_dict"]
        min_name_length: int = rd.choices(
            population=[int(pop) for pop in cities_count_by_name_length.keys()],
            weights=list(cities_count_by_name_length.values()),
            k=1,
        )[0]
        letters_queue = deque([" "] * (Config.CONTEXT_LENGTH - 1))
        city_name = " " * Config.CONTEXT_LENGTH

        # Generate city name by picking letters based on the distribution dict
        for idx in range(Config.MAX_CITY_LENGTH):
            tmp_distrib_dict = distribution_dict[letters_queue[0]]
            for i in range(1, Config.CONTEXT_LENGTH - 1):
                tmp_distrib_dict = tmp_distrib_dict[letters_queue[i]]
            # Pick the next letter
            next_letter = rd.choices(
                population=list(tmp_distrib_dict.keys()),
                weights=list(tmp_distrib_dict.values()),
                k=1,
            )[0]

            # Are we done yet?
            if next_letter == " " and (city_name[-1] == " " or idx >= min_name_length):
                # We're done, time to stop this iteration
                final_name = reformat_name(city_name)
                if is_valid(final_name):
                    # We have a valid name!
                    city_name = final_name
                    continue_generation = False
                break

            # Add the new letter to the city name
            city_name += next_letter
            letters_queue.append(next_letter)
            letters_queue.popleft()

    return city_name, region_cache["region_name"]  # NOQA


def generate_tweet():
    """
    Generates a tweet, consisting of:
        - A city name
        - The region it's located in
        - Its population
    """
    # City name generation
    city_name, region_name = generate_new_city_name()
    tweet_str = emojize(f":houses: {city_name}\n")
    tweet_str += emojize(f":national_park: {region_name}\n")

    # Population
    population = round(rd.expovariate(lambd=Config.POPULATION_LAMBDA) + 1)
    tweet_str += emojize(f":man: {population} habitants")

    return tweet_str, city_name, region_name, population

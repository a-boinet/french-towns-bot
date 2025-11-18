import binascii
import datetime
import os
import time
import zlib
from collections import deque
from pathlib import Path

try:
    import ujson as json
except ImportError:
    import json

from tqdm import tqdm

from src.config import Config


MAIN_CACHE_FILE_PATH = Config.CACHE_DIR / "main_cache.json"


def generate_all_cache_files():
    start_time = time.time()
    print("Generating all cache files...")
    cities_count_by_region: dict[str, int] = {}
    tqdm_loop = tqdm(
        os.listdir(Config.RESOURCES_DIR / "cities_by_region"),
        desc="Generating cache files for each region",
    )
    for region_file_name in tqdm_loop:
        region_name = region_file_name.removesuffix(".txt")
        tqdm_loop.set_description(f"Generating for {region_name}")
        region_data = generate_and_save_cache_for_region(region_name)
        cities_count_by_region[region_name] = region_data["cities_count"]
    main_cache_data = {
        "generated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cities_count_by_region": cities_count_by_region,
    }
    write_data_to_file(
        main_cache_data, file_path=MAIN_CACHE_FILE_PATH, compress_data=False
    )
    print(
        f"Generation done in {time.time() - start_time:.1f} sec. "
        f"All files have been saved to {Config.CACHE_DIR}"
    )


def get_cache_file_path_from_region_name(region_name: str) -> Path:
    return Config.CACHE_DIR / f"{region_name}.zlib"


def generate_and_save_cache_for_region(region_name: str) -> dict:
    with open(Config.BASE_DIR / f"resources/cities_by_region/{region_name}.txt") as f:
        # Get the cities list
        cities_list = [city.strip().lower() for city in f.readlines()]
    # Generate the statistical distribution for this region
    distribution_dict, alphabet, cities_count_by_name_length = (
        generate_distribution_dict(cities_list)
    )
    # Dump the data into a cache file
    data = {
        "region_name": region_name,
        "cities_count": len(cities_list),
        "alphabet": alphabet,
        "cities_count_by_name_length": cities_count_by_name_length,
        "distribution_dict": distribution_dict,
    }
    write_data_to_file(
        data, file_path=get_cache_file_path_from_region_name(region_name)
    )
    return data


def get_alphabet_from_word_list(word_list: list[str]) -> str:
    alphabet = {" "}  # Make the space part of the alphabet by default
    for word in set(word_list):
        for char in word:
            if char not in alphabet:  # Faster than trying to add every char by default
                alphabet.add(char)
    return "".join(sorted(alphabet))


def get_empty_distribution_dict(alphabet: str, context_length: int) -> dict:
    assert context_length >= 1
    if context_length == 1:
        return {letter: 0 for letter in alphabet}
    d = {}
    for letter in alphabet:
        d[letter] = get_empty_distribution_dict(alphabet, context_length - 1)
    return d


def generate_distribution_dict(
    word_list: list[str],
) -> tuple[dict, str, dict[int, int]]:
    alphabet = get_alphabet_from_word_list(word_list)
    distribution_dict = get_empty_distribution_dict(
        alphabet, context_length=Config.CONTEXT_LENGTH
    )
    cities_count_by_name_length: dict[int, int] = {}
    for word in word_list:
        # Increment `cities_count_by_name_length` for the current length
        if len(word) not in cities_count_by_name_length:
            cities_count_by_name_length[len(word)] = 0
        cities_count_by_name_length[len(word)] += 1
        # Update distribution dict for this city name
        context_window = deque([" "] * Config.CONTEXT_LENGTH)
        word += " " * (Config.CONTEXT_LENGTH - 1)
        for character in word:
            context_window.popleft()
            context_window.append(character)
            value = distribution_dict[context_window[0]]
            for i in range(1, Config.CONTEXT_LENGTH - 1):
                value = value[context_window[i]]
            value[context_window[Config.CONTEXT_LENGTH - 1]] += 1
    return distribution_dict, alphabet, cities_count_by_name_length


def write_data_to_file(data: dict, file_path: Path, compress_data: bool = True):
    try:
        os.mkdir(file_path.parent)
    except FileExistsError:
        pass
    if compress_data:
        write_mode = "wb"
        data_to_write = zlib.compress(
            binascii.hexlify(bytes(json.dumps(data).encode())), level=9
        )
    else:
        write_mode = "w"
        data_to_write = json.dumps(data)
    # Write data to file
    with open(file_path, write_mode) as f:
        f.write(data_to_write)


def read_data_from_file(file_path: Path, data_is_compressed: bool = True) -> dict:
    with open(file_path, "rb" if data_is_compressed else "r") as f:
        data = f.read()
    if data_is_compressed:
        # Decompress and decode the data
        data = zlib.decompress(data)
        data = binascii.unhexlify(data).decode("utf8")
    # Load the data dict
    data = json.loads(data)
    return data


if __name__ == "__main__":
    generate_all_cache_files()

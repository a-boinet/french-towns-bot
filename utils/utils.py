import zlib
import json
import binascii
import time
import random as rd
import regex as re
from os import mkdir
from collections import deque


ALPHABET_FR = " abcdefghijklmnopqrstuvwxyz-'àéâèêëîïôûüÿç"
FRENCH_CITIES_COUNT_BY_NAME_LENGTH = [
    1,
    15,
    160,
    778,
    2127,
    3469,
    3932,
    3935,
    3185,
    2612,
    1944,
    1477,
    1219,
    1039,
    1155,
    1221,
    1176,
    1227,
    1150,
    1035,
    968,
    834,
    684,
    519,
    345,
    213,
    105,
    53,
    50,
    24,
    11,
    9,
    2,
    4,
    6,
    2,
    2,
    3,
    0,
    4,
    2,
    0,
    1,
    1,
    1,
]


def get_list_from_file(file_name, separator="\n"):
    return [
        item.strip('"').strip("'")
        for item in open(file_name, "r").read().split(separator)
    ]


def write_distrib_dict_to_file(file_path, distrib_dict):
    # data = str([alphabet, mean_length, distrib_dict])
    data = distrib_dict
    compressed_data = zlib.compress(binascii.hexlify(bytes(str.encode(data))), 9)
    file = open(file_path, "wb")
    file.write(compressed_data)
    file.close()


def generate_distrib_dict(name_list, file_path, alphabet=ALPHABET_FR):
    """
    Returns a distribution dictionnary and writes it in distrib_dict.txt

    :param name_list: A list of all the names given as examples
    :param dict_name: The name you want to give to the dict
    :param alphabet: The alphabet that will be used to create
                     the distribution dictionnary
    """
    print("Running...")
    distrib_dict = {}
    n = len(alphabet)
    for i in range(n):
        distrib_dict[alphabet[i]] = {}
        for j in range(n):
            distrib_dict[alphabet[i]][alphabet[j]] = {}
            for k in range(n):
                distrib_dict[alphabet[i]][alphabet[j]][alphabet[k]] = {}
                for l in range(n):
                    distrib_dict[alphabet[i]][alphabet[j]][alphabet[k]][alphabet[l]] = 0
    for name in name_list:
        idx = deque([" ", " ", " ", " "])
        name += "   "
        for character in name:
            idx.popleft()
            idx.append(character)
            distrib_dict[idx[0]][idx[1]][idx[2]][idx[3]] += 1
    json_dict = json.dumps(distrib_dict)
    try:
        mkdir("./utils/regions_france_dict")
    except FileExistsError:
        pass
    print("Generation done, writing file\n")
    write_distrib_dict_to_file(
        file_path=file_path, distrib_dict=json_dict,
    )


def read_distrib_dict_from_file(file_name):
    file = open(file_name, "rb")
    compressed_data = file.read()
    decompressed_data = zlib.decompress(compressed_data)
    decompressed_data = binascii.unhexlify(decompressed_data).decode("utf8")
    decompressed_data = json.loads(decompressed_data)
    return decompressed_data


def is_correct(word, name_list_source=None, fr_dict=None):
    """
    Helps finding out if name sounds french or not
    :returns: True or False
    """
    word = word.lower()
    pattern_word = " " + word + " "
    if name_list_source is None:
        name_list_source = []
    if fr_dict is None:
        fr_dict = []
    # Must be 4 letters or more
    forbidden_words = open("./res/forbidden_words.txt", "r").read().split("\n")
    forbidden_words.pop()
    forbidden_patterns = open("./res/forbidden_patterns.txt", "r").read().split("\n")
    forbidden_patterns.pop()
    contains_forbidden_pattern = False
    for fp in forbidden_patterns:
        if fp in pattern_word:
            contains_forbidden_pattern = True
    contains_long_word = False
    for chunk in word.split("-"):
        if len(chunk) > 12:
            contains_long_word = True
    return (
        word not in forbidden_words
        and word not in name_list_source
        and word not in fr_dict
        and not contains_forbidden_pattern
        and not contains_long_word
        and not word.startswith("x")  # Doesn't sound french
        and len(word) < 30
        and len(word) > 4
        and word.count("-") < 5
    )


def intersperse(lst, item):
    # From Stack Overflow
    # https://stackoverflow.com/a/6300649/8286364
    result = [item] * (2 * len(lst) - 1)
    result[::2] = lst
    return result


def reformat_string(v_string):
    """
    Takes a string like "l'aDResse-SuR-MeR"
    and returns "l'Adresse-Sur-Mer"
    """
    # Removing whitespaces
    v_string = v_string.strip()
    # Split using "-"
    v_string = v_string.lower().split("-")
    v_string = intersperse(v_string, "-")
    words_1 = []
    for element in v_string:
        words_1.extend(intersperse(element.split("'"), "'"))
    words_2 = []
    for element in words_1:
        words_2.extend(intersperse(element.split(" "), " "))
    final_string = ""
    for word in words_2:
        final_string += word.capitalize()
    # Delete repeting patterns
    final_string = re.sub(r"(.+?)\1+", r"\1", final_string)
    replace_list = open("./res/replace_patterns.txt", "r").read().split("\n")
    replace_list.pop()
    for i in range(len(replace_list)):
        replace_list[i] = replace_list[i].split(",")
    for rep in replace_list:
        final_string = final_string.replace(rep[0], rep[1])
    return final_string


def create_words(
    distrib_dict, name_list_source=None, mean_length=12, number_of_words=100, seed=None
):
    fr_dict_list = open("dict_from_hbenbel_French-Dictionary.txt", "r").read()
    fr_dict_list = fr_dict_list.split("\n")
    fr_dict_list.pop()
    if seed is None:
        seed = time.time()
    rd.seed(seed)
    words = []
    for i in range(number_of_words):
        valid = False
        while not valid:
            min_len = rd.choices(
                population=range(45), weights=FRENCH_CITIES_COUNT_BY_NAME_LENGTH
            )[0]
            # min_len = rd.gauss(mean_length, round(mean_length/3))
            idx = deque([" ", " ", " "])
            word = "    "
            counter = 0
            space_counter = 0
            keep_going = True
            while keep_going:
                tmp_dict = distrib_dict[idx[0]][idx[1]][idx[2]]
                next_choice = rd.choices(
                    population=list(tmp_dict.keys()),
                    weights=[tmp_dict[element] for element in tmp_dict],
                )
                if next_choice[0] == " ":
                    if space_counter == 2 or counter >= min_len:
                        keep_going = False
                    space_counter += 1
                word += next_choice[0]
                idx.append(next_choice[0])
                idx.popleft()
                counter += 1
            new_name = reformat_string(word)
            if is_correct(
                word=new_name, name_list_source=name_list_source, fr_dict=fr_dict_list
            ):
                words.append(new_name)
                valid = True
            # print(new_name)
    return words

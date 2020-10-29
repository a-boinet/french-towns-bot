import pathlib
import random as rd
from emoji import emojize
from time import sleep

from utils.utils import (
    read_distrib_dict_from_file,
    get_list_from_file,
    create_words,
)

# from create_person import create_person
from utils.twitter_store import TwitterStore

REGION_DICT = {
    "Auvergne-Rhône-Alpes": [4189],
    "Bourgogne-Franche-Comté": [3831],
    "Bretagne": [1270],
    "Centre-Val de Loire": [1842],
    "Corse": [360],
    "Grand Est": [5192],
    # "Guadeloupe": [34],
    # "Guyane": [22],
    "Hauts-de-France": [3836],
    "Ile-de-France": [1281],
    # "La Réunion": [24],
    # "Martinique": [34],
    # "Mayotte": [17],
    "Normandie": [3232],
    "Nouvelle-Aquitaine": [4505],
    "Occitanie": [4565],
    "Pays de la Loire": [1502],
    "Provence-Alpes-Côte d'Azur": [963],
}

"""
The population is generated using an exponential distribution
For France, the approximate lambda is 0.0009
"""
POPULATION_LAMBDA = 0.0009


def generate_tweet():
    """
    Generates a tweet, consisting of:
        - A city name
        - The region where it is situated
        - Its population
        # - A mayor
    """
    # Region
    region = rd.choices(
        population=list(REGION_DICT.keys()),
        weights=[REGION_DICT[key][0] for key in REGION_DICT.keys()],
    )[0]

    # City name generation
    try:
        distribution_dict = read_distrib_dict_from_file(
            f"{pathlib.Path(__file__).parent.absolute()}/resources/regions_france_dict/distrib_dict_"
            + region.replace("'", "-")
            + ".zlib"
        )
    except:
        msg = f"\n\n\033[1m\033[91m[ERROR] Couldn't read distribution dictionary for {region}\033[0m\n\n"
        msg += "\033[91mDid you forget to run 'create_zlib_dicts.py'?\033[0m"
        raise Exception(msg)
    name_list = get_list_from_file(
        f"{pathlib.Path(__file__).parent.absolute()}/resources/regions_france/all_cities.txt"
    )
    city_name = create_words(
        distrib_dict=distribution_dict, name_list_source=name_list, number_of_words=1
    )[0]
    ret_str = emojize(f":houses: {city_name}\n")
    ret_str += emojize(f":national_park: {region}\n")

    # Population
    population = round(rd.expovariate(lambd=POPULATION_LAMBDA) + 1)
    ret_str += emojize(f":adult: {population} habitants")

    # # Mayor
    # mayor = create_person()
    # titre = "M." if mayor.gender == 1 else "Mme."
    # print(f"{titre} {mayor.prenom} {mayor.nom}, {mayor.age} ans")

    return ret_str


if __name__ == "__main__":
    while True:
        tw_store = TwitterStore()
        tweet_txt = generate_tweet()
        print(tweet_txt)
        ret_value = tw_store.tweet(text_to_tweet=tweet_txt)
        print("Tweeted!\n")
        # input("\n")
        sleep(60 * 60 * 8)  # 8 hours

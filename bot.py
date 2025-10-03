import pathlib
import random as rd
import traceback

from emoji import emojize
from time import sleep
from datetime import datetime

from utils.utils import (
    read_distrib_dict_from_file,
    get_list_from_file,
    create_words,
)
from utils.discord_notify import DiscordNotifier

from utils.twitter_store import TwitterStore


# Some regions are commented because the lack of training material yields poor result
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
        msg = f"\n\n\033[1m\033[91m\033[1m\033[91m[ERROR]\033[0m "
        msg += f"Couldn't read distribution dictionary for {region}\033[0m\n\n"
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
    ret_str += emojize(f":man: {population} habitants")

    return ret_str


if __name__ == "__main__":
    # We run it only once, a systemd timer should be used to run it periodically
    date_str = None
    try:
        discord_notifier = DiscordNotifier()
    except Exception as e:  # NOQA
        discord_notifier = None
    while True:
        try:
            date_str = f"{datetime.now().strftime('%d %B %Y - %H:%M')}\n"
            print(date_str)
            tw_store = TwitterStore()
            tweet_txt = generate_tweet()
            print(tweet_txt)
            # Tweet the town of the day!
            tweet_url = tw_store.tweet(text_to_tweet=tweet_txt)
            print(f"Tweet sent successfully! ({tweet_url})")
            break
        except Exception as e:  # NOQA
            tb = traceback.format_exc()
            try:
                discord_notifier.log_error(date_str, tb)
                print("Error notified on discord\n")
            except Exception as e:  # NOQA
                print(
                    "\033[1m\033[91m[ERROR]\033[0m Could not notify error on discord!"
                )
                if discord_notifier is None:
                    print("\t`discord_notifier` is `None`")
            print(tb)
            sleep(30 * 60 * 1)  # 30 minutes

    # Notify on discord
    try:
        discord_notifier.notify_tweet(tweet_url=tweet_url)
        print("Tweet notified on discord\n")
    except Exception as e:  # NOQA
        print("\033[1m\033[91m[ERROR]\033[0m Could not notify tweet on discord!")
        if discord_notifier is None:
            print("\t`discord_notifier` is `None`")
        else:
            tb = traceback.format_exc()
            print(tb)

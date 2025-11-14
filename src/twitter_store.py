import os
import pathlib
import random
import tweepy

KEYS_FILE = f"{pathlib.Path(__file__).parent.absolute()}/twitter_keys.txt"
KEYS_DICT: dict[str, str] = {}

if not os.path.exists(KEYS_FILE):
    error_msg = (
        f"\n\n\033[1m\033[91m[ERROR] {KEYS_FILE} not found\033[0m\n\n"
        f"\033[91mIt looks like you didn't create 'utils/twitter_keys.txt' "
        f"(see README.md for expected format)\033[0m\n"
    )
    raise FileNotFoundError(error_msg)

try:
    with open(KEYS_FILE, "r") as f:
        for line in f.readlines():
            k, v = line.removesuffix("\n").split("=")
            KEYS_DICT[k] = v.strip('"').strip("'")
    assert "CONSUMER_KEY" in KEYS_DICT.keys(), "Missing 'CONSUMER_KEY'"
    assert "CONSUMER_SECRET" in KEYS_DICT.keys(), "Missing 'CONSUMER_SECRET'"
    assert "ACCESS_TOKEN" in KEYS_DICT.keys(), "Missing 'ACCESS_TOKEN'"
    assert "ACCESS_TOKEN_SECRET" in KEYS_DICT.keys(), "Missing 'ACCESS_TOKEN_SECRET'"
except:  # NOQA
    error_msg = (
        "\n\n\033[1m\033[91m[ERROR] Couldn't retrieve Twitter API Tokens\033[0m\n\n"
        "\033[91mIs the format compliant with README.md instructions?\033[0m\n"
    )
    raise Exception(error_msg)


class TwitterStore:
    def __init__(self):
        self._client = tweepy.Client(
            consumer_key=KEYS_DICT["CONSUMER_KEY"],
            consumer_secret=KEYS_DICT["CONSUMER_SECRET"],
            access_token=KEYS_DICT["ACCESS_TOKEN"],
            access_token_secret=KEYS_DICT["ACCESS_TOKEN_SECRET"],
        )

    def tweet(self, text_to_tweet) -> str:
        _response = self._client.create_tweet(text=text_to_tweet)
        _tweet_url = f"https://x.com/twitter/status/{_response.data['id']}"
        return _tweet_url


if __name__ == "__main__":
    ts = TwitterStore()
    input_value = input("Type 'yes' or 'y' to send a test tweet: ")
    if input_value.lower() in ["y", "yes"]:
        tweet_url = ts.tweet(f"Hello world! This is a test - {random.random()}")
        print(tweet_url)
    else:
        print("Ok, test tweet not sent")

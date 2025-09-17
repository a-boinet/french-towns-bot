import tweepy
import random
import pathlib

try:
    keys = open(
        f"{pathlib.Path(__file__).parent.absolute()}/twitter_keys.txt", "r"
    ).readlines()

    CONSUMER_KEY = keys[0].strip("\n").split("=")
    assert CONSUMER_KEY[0] == "CONSUMER_KEY", "Bad format for CONSUMER_KEY"
    CONSUMER_KEY = CONSUMER_KEY[1].strip('"')

    CONSUMER_SECRET = keys[1].strip("\n").split("=")
    assert CONSUMER_SECRET[0] == "CONSUMER_SECRET", "Bad format for CONSUMER_SECRET"
    CONSUMER_SECRET = CONSUMER_SECRET[1].strip('"')

    ACCESS_TOKEN = keys[2].strip("\n").split("=")
    assert ACCESS_TOKEN[0] == "ACCESS_TOKEN", "Bad format for ACCESS_TOKEN"
    ACCESS_TOKEN = ACCESS_TOKEN[1].strip('"')

    ACCESS_TOKEN_SECRET = keys[3].strip("\n").split("=")
    assert (
        ACCESS_TOKEN_SECRET[0] == "ACCESS_TOKEN_SECRET"
    ), "Bad format for ACCESS_TOKEN_SECRET"
    ACCESS_TOKEN_SECRET = ACCESS_TOKEN_SECRET[1].strip('"')
except:
    msg = "\n\n\033[1m\033[91m[ERROR] Couldn't retrieve Twitter API Tokens\033[0m\n\n"
    msg += "\033[91mDid you forget to create 'utils/twitter_keys.txt'?\033[0m"
    raise Exception(msg)


class TwitterStore:
    def __init__(self):
        self._client = tweepy.Client(
            consumer_key=CONSUMER_KEY,
            consumer_secret=CONSUMER_SECRET,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_TOKEN_SECRET,
        )

    def tweet(self, text_to_tweet) -> str:
        _response = self._client.create_tweet(text=text_to_tweet)
        _tweet_url = f"https://x.com/twitter/status/{_response.data['id']}"
        return _tweet_url


if __name__ == "__main__":
    input("Press enter to send a test tweet\n")
    ts = TwitterStore()
    tweet_url = ts.tweet(f"Hello world! This is a test - {random.random()}")
    print(tweet_url)

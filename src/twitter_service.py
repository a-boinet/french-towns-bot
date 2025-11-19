import random
import tweepy

from src.keys import Keys


def send_tweet(text_to_tweet: str) -> str:
    client = tweepy.Client(
        consumer_key=Keys.CONSUMER_KEY,
        consumer_secret=Keys.CONSUMER_SECRET,
        access_token=Keys.ACCESS_TOKEN,
        access_token_secret=Keys.ACCESS_TOKEN_SECRET,
    )
    response = client.create_tweet(text=text_to_tweet)
    tweet_url = f"https://x.com/twitter/status/{response.data['id']}"
    return tweet_url


if __name__ == "__main__":
    input_value = input("Type 'yes' or 'y' to send a test tweet: ")
    if input_value.lower() in {"y", "yes"}:
        test_tweet_url = send_tweet(f"Hello world! This is a test - {random.random()}")
        print(test_tweet_url)
    else:
        print("Ok, test tweet not sent")

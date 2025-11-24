import traceback

from time import sleep
from datetime import datetime

from src.config import Config
from src.generator import generate_tweet
from src.twitter_service import send_tweet
from src.discord_service import DiscordNotifier
from src.validator import save_city_name


if __name__ == "__main__":
    # We run it only once.
    # A systemd timer / cron job should be used to run it periodically.
    while True:
        date_str = f"{datetime.now().strftime('%d %B %Y - %H:%M')}"
        print(date_str, "\n")
        try:
            # Generate city name
            tweet_txt, city_name, _, _ = generate_tweet()
            print(tweet_txt)
            # Tweet the town of the day!
            tweet_url = send_tweet(text_to_tweet=tweet_txt)
            print(f"Tweet sent successfully! ({tweet_url})")
            # Now that the tweet was sent, let's save the town name
            # to the `already_tweeted.txt` file (so we don't tweet it twice)
            save_city_name(city_name)
            break
        except:  # NOQA
            tb = traceback.format_exc()
            try:
                DiscordNotifier.log_error(date_str, tb)
                print("Error notified on discord\n")
            except:  # NOQA
                print(
                    "\033[1m\033[91m[ERROR]\033[0m Could not notify error on discord!"
                )
            print(tb)
            sleep(Config.WAIT_TIME_BEFORE_RETRY)  # 30 minutes

    # Notify on discord
    try:
        DiscordNotifier.notify_tweet(tweet_url=tweet_url)
        print("Tweet notified on discord\n")
    except:  # NOQA
        print("\033[1m\033[91m[ERROR]\033[0m Could not notify tweet on discord!")

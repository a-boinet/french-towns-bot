import os
import pathlib
import warnings
from discord_webhook import DiscordWebhook, DiscordEmbed

URL_FILE = f"{pathlib.Path(__file__).parent.absolute()}/discord_url.txt"
URL_DICT: dict[str, str] = {}

if not os.path.exists(URL_FILE):
    error_msg = (
        f"\n\n\033[1m\033[91m[ERROR] {URL_FILE} not found\033[0m\n\n"
        f"\033[91mIt looks like you didn't create 'utils/discord_url.txt' "
        f"(see README.md for expected format)\033[0m\n"
    )
    warnings.warn(error_msg, Warning)
else:
    try:
        with open(URL_FILE, "r") as f:
            for line in f.readlines():
                k, v = line.removesuffix("\n").split("=")
                URL_DICT[k] = v.strip('"').strip("'")
        assert "TWEET_LOG_URL" in URL_DICT.keys(), "Missing 'TWEET_LOG_URL'"
        assert "ERROR_LOG_URL" in URL_DICT.keys(), "Missing 'ERROR_LOG_URL'"
    except:  # NOQA
        error_msg = (
            "\n\n\033[1m\033[91m[ERROR] Couldn't retrieve Discord URL\033[0m\n\n"
            "\033[91mIs the format compliant with README.md instructions?\033[0m\n"
        )
        warnings.warn(error_msg, SyntaxWarning)


class DiscordNotifier:
    def __init__(self):
        self._tweet_log_url = URL_DICT["TWEET_LOG_URL"]
        self._error_log_url = URL_DICT["ERROR_LOG_URL"]

    def notify_tweet(self, tweet_url: str):
        webhook = DiscordWebhook(url=self._tweet_log_url, content=tweet_url)
        webhook.execute()

    def log_error(self, date, tb):
        webhook = DiscordWebhook(
            url=self._error_log_url, content=f"Error caught on {date}{tb}"
        )
        webhook.execute()

    def report_error(self, exception, tb):
        # TODO Continue (?)
        embed = DiscordEmbed(
            title=f"Error {repr(exception)}",
            footer={
                "text": tb,
                "icon_url": None,
                "proxy_icon_url": None,
                # "icon_url": "https://pbs.twimg.com/profile_images/1263231399240380418/lIbJaPnf_400x400.jpg",
                # "proxy_icon_url": "https://pbs.twimg.com/profile_images/1263231399240380418/lIbJaPnf_400x400.jpg",
            },
            color="ff0000",
        )
        webhook = DiscordWebhook(
            url=self._url,
        )
        webhook.add_embed(embed)
        webhook.execute()

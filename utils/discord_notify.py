import pathlib
from discord_webhook import DiscordWebhook, DiscordEmbed

with open(f"{pathlib.Path(__file__).parent.absolute()}/discord_url.txt", "r") as file:
    lines = file.readlines()

URL_TWEET = lines[0].strip("\n").split("=")
assert URL_TWEET[0] == "TWEET", "Bad format for TWEET webhook"
URL_TWEET = URL_TWEET[1].strip('"')

URL_TWEET_LOGS = lines[1].strip("\n").split("=")
assert URL_TWEET_LOGS[0] == "TWEET_LOGS", "Bad format for TWEET_LOGS webhook"
URL_TWEET_LOGS = URL_TWEET_LOGS[1].strip('"')


class DiscordNotifier:
    def __init__(self, url):
        self._url = url

    def notify_tweet(self, twitter_store_response):
        webhook = DiscordWebhook(
            url=self._url,
            content=f"https://twitter.com/twitter/statuses/{twitter_store_response.id_str}",
        )
        webhook.execute()

    def report_log_tmp(self, date, tb):
        webhook = DiscordWebhook(url=self._url, content=f"Error caught on {date}{tb}")
        webhook.execute()

    def report_error(self, exception, tb):
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
        webhook = DiscordWebhook(url=self._url,)
        webhook.add_embed(embed)
        webhook.execute()

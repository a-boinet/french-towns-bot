import pathlib
from discord_webhook import DiscordWebhook, DiscordEmbed


class DiscordNotifier:
    def __init__(self, url=None):
        if url is None:
            with open(
                f"{pathlib.Path(__file__).parent.absolute()}/discord_url.txt", "r"
            ) as file:
                url = file.readlines()[0].strip("\n")
        self._url = url

    def notify_tweet(self, twitter_store_response):
        webhook = DiscordWebhook(
            url=self._url,
            content=f"https://twitter.com/twitter/statuses/{twitter_store_response.id_str}",
        )
        webhook.execute()

    def report_error(self, error):
        pass

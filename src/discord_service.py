import warnings

from discord_webhook import DiscordWebhook

from src.config import Keys


class DiscordNotifier:
    @staticmethod
    def _notify(webhook_url: str, content: str):
        if webhook_url is None:
            warnings.warn("Webhook URL is None - Not notified on discord!")
            return
        webhook = DiscordWebhook(url=webhook_url, content=content)
        webhook.execute()

    @staticmethod
    def notify_tweet(tweet_url: str):
        DiscordNotifier._notify(webhook_url=Keys.TWEET_LOG_URL, content=tweet_url)

    @staticmethod
    def log_error(date: str, tb: str):
        DiscordNotifier._notify(
            webhook_url=Keys.ERROR_LOG_URL, content=f"Error caught on {date}\n{tb}"
        )

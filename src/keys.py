import os
import warnings

from src.config import Config


class KeyDict(dict):
    """
    Allows the use of `d.k` instead of `d['k']`
    Return None if key does not exist
    """

    __setattr__ = dict.__setitem__

    def __getattr__(self, key):
        return dict.get(self, key)

    def __getitem__(self, key):
        return dict.get(self, key)


KEYS_FILE = Config.BASE_DIR / "keys.txt"
if not os.path.exists(KEYS_FILE):
    raise FileNotFoundError(
        f"\033[1m\033[91m[ERROR] {KEYS_FILE} not found\033[0m\n\n"
        f"\033[91mIt looks like you didn't create 'keys.txt' "
        f"(see README.md for more information)\033[0m"
    )

# The dict storing all the API keys and webhook URLs
Keys = KeyDict()

with open(KEYS_FILE, "r") as f:
    for line in f.readlines():
        k, v = line.strip().split("=")
        Keys[k] = v.strip('"').strip("'")

# Check that we have the required Twitter API keys
assert (
    "CONSUMER_KEY" in Keys.keys()
), "Missing 'CONSUMER_KEY' (see README.md for more information)"
assert (
    "CONSUMER_SECRET" in Keys.keys()
), "Missing 'CONSUMER_SECRET' (see README.md for more information)"
assert (
    "ACCESS_TOKEN" in Keys.keys()
), "Missing 'ACCESS_TOKEN' (see README.md for more information)"
assert (
    "ACCESS_TOKEN_SECRET" in Keys.keys()
), "Missing 'ACCESS_TOKEN_SECRET' (see README.md for more information)"

# Check for optional discord webhook URLS
if "TWEET_LOG_URL" not in Keys.keys():
    warnings.warn(
        "\033[1m\033[91m[ERROR] Couldn't retrieve Discord URL to notify new tweets\033[0m"
    )
if "ERROR_LOG_URL" not in Keys.keys():
    warnings.warn(
        "\033[1m\033[91m[ERROR] Couldn't retrieve Discord URL to notify errors\033[0m"
    )

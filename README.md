# French Towns Bot
A Twitter bot that creates french-sounding city names

<img src="./img/logo.jpg" alt="French Towns Bot logo" align="right" width="200">

<a href="https://twitter.com/intent/follow?screen_name=FrenchTownsBot">
  <img src="https://img.shields.io/twitter/follow/FrenchTownsBot?style=social&logo=twitter"
    alt="Follow this bot on Twitter" title="Follow this bot on Twitter">
</a>

## Table of Contents

1. [Setup](#setup)
2. [Run](#run)
3. [How it works](#how-it-works)
4. [Git hook installation](#git-hook-installation)
5. [License](#license)

## Setup

First, let's install the required modules:
```bash
pip install -r requirements.txt
```

If you just want to try the name generation, you can run

```bash
python playground.py
```

To be able to post on Twitter, you must provide the bot with your Twitter API Tokens:
```bash
nano keys.txt  # Create the file in the root directory
```
The expected format for `keys.txt` is:
```bash (not actually bash, but easier to read)
CONSUMER_KEY=your_CONSUMER_KEY_here
CONSUMER_SECRET=your_CONSUMER_SECRET_here
ACCESS_TOKEN=your_ACCESS_TOKEN_here
ACCESS_TOKEN_SECRET=your_ACCESS_TOKEN_SECRET_here
```

_Optional:_ You can connect the bot to a discord channel in order to get notified for new tweets and errors. You can add the webhook URLs to `keys.txt`. The expected format is:
```bash (not actually bash, but easier to read)
TWEET_LOG_URL=your_DISCORD_WEBHOOK_here
ERROR_LOG_URL=your_DISCORD_WEBHOOK_here
```


## Run

```bash
python bot.py
```

## How it works

Inspired by this video: https://www.youtube.com/watch?v=YsR7r2378j0

## Git hook installation

If you're planning on contributing to this project, you can enable the pre-commit git hook (allowing code formatting with [Black](https://github.com/psf/black), among other things):
```bash
./install-githook.sh
```

## License
Usage is provided under the [GPL-3.0 License ](https://www.gnu.org/licenses/gpl-3.0.en.html). See LICENSE for the full details.

The file [`french_dictionary.txt`](./resources/french_dictionary.txt) was adapted from [French-Dictionary](https://github.com/hbenbel/French-Dictionary) (under MIT License), by [Hussem Ben Belgacem](https://github.com/hbenbel).

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

In order to generate city names, the bot will need what I called *distribution dictionaries* (check out the [How it works](#how-it-works) section for more information).

Run the following script:

```bash
python create_zlib_dicts.py
```

To be able to post on Twitter, you must provide the bot with your Twitter API Tokens:
```bash
nano utils/twitter_keys.txt
```
The expected format for `utils/twitter_keys.txt` is:
```bash (not actually bash, but easier to read)
CONSUMER_KEY=your_CONSUMER_KEY_here
CONSUMER_SECRET=your_CONSUMER_SECRET_here
ACCESS_TOKEN=your_ACCESS_TOKEN_here
ACCESS_TOKEN_SECRET=your_ACCESS_TOKEN_SECRET_here
```

## Run

```bash
python bot.py
```

## How it works

TODO

## Git hook installation

If you're planning on contributing to this project, you can enable the pre-commit git hook (allowing code formatting with [Black](https://github.com/psf/black), among other things):
```bash
./install-githook.sh
```

## License
Usage is provided under the [GPL-3.0 License ](https://www.gnu.org/licenses/gpl-3.0.en.html). See LICENSE for the full details.

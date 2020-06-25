# French Towns Bot
A Twitter bot that creates french-sounding city names

## Table of Contents

1. [Setup](#setup)
2. [Git hook installation](#git-hook-installation)

## Setup

First, let's install the required modules:
```bash
python install -r requirements.txt
```
To be able to post on Twitter, you must provide the bot with your Twitter API Tokens
(otherwise you will get an error):
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

Once you have done that, you are good to go!
```bash
python bot.py
```

## Git hook installation

If you're planning on contributing to this project, you can enable the pre-commit git hook (allowing code formatting with [Black](https://github.com/psf/black), among other things):
```bash
./install-githook.sh
```

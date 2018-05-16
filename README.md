# VibrationBot
VibrationBot is a Telegram bot that vibrates images. You can access the bot at [@VibrationBot](http://t.me/VibrationBot).

## Dependencies
The bot runs on [Python 3](http://python.org) and some libraries. Install the following using `pip install <name>`:

* [Python Telegram Bot](http://python-telegram-bot.org): `python-telegram-bot`
* [Pillow](https://pillow.readthedocs.io): `Pillow`
* [Fasteners](https://fasteners.readthedocs.io): `fasteners`

## Configuration
The bot uses JSON files for configuration. A sample with comments is provided [sample.config.json](sample.config.json). In these files you specify the Telegram bot's token, provided by the [@BotFather](http://t.me/BotFather). Perhaps you'll want to copy this file twice: `dev.config.json` and `prod.config.json`.

## Running the Bot
The file [startup.py](startup.py) will attempt to acquire a lock, then start the bot. Run the bot with the configuration file as the only command line argument, like so:

```bash
python startup.py dev.config.json
```

You can use the interrupt command to stop the bot (`CTRL+C` on Windows).

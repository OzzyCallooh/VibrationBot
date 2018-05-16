# VibrationBot
VibrationBot is a Telegram bot that vibrates images. You can access the bot at [@VibrationBot](http://t.me/VibrationBot).

## How to Use
In your favorite Telegram client, [open a chat](http://t.me) with the bot. Then, send it a photo (use the paperclip). Here are the commands:

* **/start**: Display welcome message. Required to start chatting with the bot.
* **/help**: Display help text for using the bot.
* **/about**: Display about text for more information.

* Make sure the image dimensions are from 80px to 1000px.
* By default, the bot will vibrate on 4 corners.
* Caption the image `h` or `v` (just a single, lower-case letter) to instead vibrate horizontally or vertically.

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

You can use the interrupt signal to stop the bot (`CTRL+C` on Windows).

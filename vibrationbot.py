"""
	Vibration bot!

	[vibration intensifies]
"""

import sys
import os
import logging
import telegram
import random
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from config import config
import vibrate

MIN_SIZE = config['vibration']['min_size_px']
MAX_SIZE = config['vibration']['max_size_px']

def positive_input_message():
	return random.choice(config['text']['positive_input'])

def please_wait_message():
	return random.choice(config['text']['please_wait'])

def command_start(bot, update):
	update.message.reply_text(config['text']['commands']['start'])

def command_help(bot, update):
	update.message.reply_text(config['text']['commands']['help'].format(
		min_size=MIN_SIZE, max_size=MAX_SIZE,
	))

def command_about(bot, update):
	update.message.reply_text(config['text']['commands']['about'])

def handler_photo(bot, update):
	photo_size =update.message.photo[-1]

	if photo_size.width < MIN_SIZE or photo_size.height < MIN_SIZE:
		update.message.reply_text(config['text']['error']['bad_dimensions'].format(
			min_size=MIN_SIZE, max_size=MAX_SIZE,
			width=photo_size.width, height=photo_size.height
		))
		return

	file_id = photo_size.file_id
	photo_file = bot.getFile(file_id)
	update.message.reply_text(
		positive_input_message() + ' You sent an image of size {width} by {height}. '.format(
			width=photo_size.width,
			height=photo_size.height
		) + please_wait_message()
	)

	# Save input file 
	photo_file.download()
	filename_input = photo_file.file_path.split('/')[-1]
	print('Saved input file to ' + filename_input)

	# Vibration parameters
	vibration_dist = round(min(photo_size.width, photo_size.height) * 0.02)
	vibration_mode = vibrate.MODE_CORNERS
	if update.message.caption == 'h':
		vibration_mode = vibrate.MODE_HORIZONTAL
	elif update.message.caption == 'v':
		vibration_mode = vibrate.MODE_VERTICAL

	# Do the vibration!
	filename_result = vibrate.vibrate(filename_input, vibration_mode, vibration_dist)

	print('Vibration result saved to ' + filename_result)

	# Sending a video
	bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.UPLOAD_VIDEO)
	update.message.reply_video(video=open(filename_result, 'rb'))
	update.message.reply_text(
		config['text']['result'].format(
			mode=vibration_mode,
			distance=vibration_dist
		)
	)

	# Clean up files
	os.remove(filename_input)
	os.remove(filename_result)

def main():
	updater = Updater(token=config['telegram']['token'])
	dispatcher = updater.dispatcher
	dispatcher.add_handler(CommandHandler('start', command_start))
	dispatcher.add_handler(CommandHandler('help', command_help))
	dispatcher.add_handler(CommandHandler('about', command_about))
	dispatcher.add_handler(MessageHandler(Filters.photo, handler_photo))

	logging.basicConfig(
		format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
		level=logging.DEBUG if config['debug_mode'] else logging.INFO
	)

	print('[vibrations start]')
	updater.start_polling(clean=True)
	updater.idle()
	print('[vibrations cease]')
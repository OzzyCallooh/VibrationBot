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

if len(sys.argv) < 2:
	print('Format: python ' + sys.argv[0] + ' <token>')
	sys.exit()

MIN_SIZE = 80
MAX_SIZE = 2000

MESSAGE_START = 'Hi there! Send me an image to vibrate. Use /help for more information.'
MESSAGE_HELP = 'To vibrate an image, send it to me. Images dimensions must be at least {min_size} px and at most {max_size} px. Caption your image \'v\' or \'h\' to vibrate only horizontally or vertically.'.format(min_size=MIN_SIZE, max_size=MAX_SIZE)
MESSAGE_ABOUT = 'This bot was made by @OzzyC. Please don\'t overuse it, and send questions/comments/concerns to @OzzyC.'
ERROR_BAD_DIMENSIONS = 'Sorry, images dimensions must be between {min_size} and {max_size} px. The image you sent is {width} by {height} pixels.'

def positive_input_message():
	return random.choice([
		'Looking good, mate!',
		'Awesome!'
	])

def please_wait_message():
	return random.choice([
		'Intensifing image, one moment please!',
		'Making image more intense, please wait!',
		'Vibrating image, one second please!',
		'Increasing intensity, please wait!',
	])

def command_start(bot, update):
	update.message.reply_text(MESSAGE_START)

def command_help(bot, update):
	update.message.reply_text(MESSAGE_HELP)

def command_about(bot, update):
	update.message.reply_text(MESSAGE_ABOUT)

def handler_photo(bot, update):
	photo_size =update.message.photo[-1]

	if photo_size.width < MIN_SIZE or photo_size.height < MIN_SIZE:
		update.message.reply_text(ERROR_BAD_DIMENSIONS.format(
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
		'Here is your intensified photo. Mode: {mode}, Distance: {distance} px'.format(
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
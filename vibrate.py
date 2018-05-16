# hello, pillow
from PIL import Image
from PIL import ImageSequence
#import PIL.GifImagePlugin.GifImageFile

MODE_CORNERS = 'Corners'
MODE_VERTICAL = 'Vertical'
MODE_HORIZONTAL = 'Horizontal'

def get_boxes(mode, v, size):
	w, h = size
	if mode == MODE_CORNERS:
		return ((w - v, h - v), [
			# top left
			(0, 0, w - v, h - v),
			# top right
			(v, 0, w, h - v),
			# bottom right
			(v, v, w, h),
			# bottom left
			(0, v, w - v, h),
		])
	elif mode == MODE_VERTICAL:
		return ((w, h - v), [
			# top
			(0, v, w, h),
			# bottom
			(0, 0, w, h - v),
		])
	elif mode == MODE_HORIZONTAL:
		return ((w - v, h), [
			# left
			(0, 0, w - v, h),
			# right
			(v, 0, w, h),
		])

def vibrate(filename, mode, dist):
	im = Image.open(filename)

	dimensions, boxes = get_boxes(mode, dist, im.size)
	regions = []
	for box in boxes:
		regions.append(im.crop(box))

	im_frames = []
	for region in regions:
		im_frame = Image.new(
			'RGB',
			dimensions,
			color=0
		)
		im_frame.paste(region)
		im_frames.append(im_frame)

	im_res = im_frames[0]
	filename_result = filename.split('.')[0] + '.gif'
	im_res.save(filename_result, 'GIF',
		save_all=True,
		append_images=im_frames[1:],
		duration=25,
		loop=0,
	)
	print('GIF Vibrate Result:', im_res.format, im_res.size, im_res.mode)
	return filename_result

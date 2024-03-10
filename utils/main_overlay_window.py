from time import time

import cv2 as cv

from config.config_manager import ConfigManager
from utils.read_json import read_json
from vision import Vision
from windowcapture import WindowCapture

config_manager = ConfigManager()

assets_data = read_json(config_manager.get_value('config.assets_data'))


def load_image_path():
	for name, path in assets_data['images'].items():
		if path is not None:
			image_path = path
			vision = Vision(image_path)
			return vision


def overlay_window():
	# initialize the WindowCapture class
	wincap = WindowCapture('Dual Universe')

	# initialize the Vision class
	# vision_limestone = Vision(
	# 	"C:\\Repositories\\Dual Universe\\Missions Dual Universe\\data\\images\\Air_Yordans.png")  # TODO: feed in images from image directory

	'''
	# https://www.crazygames.com/game/guns-and-bottle
	wincap = WindowCapture()
	vision_gunsnbottle = Vision('gunsnbottle.jpg')
	'''

	loop_time = time()
	while True:

		# get an updated image of the game
		screenshot = wincap.get_screenshot()

		vision = load_image_path()
		# display the processed image
		points = vision.find(screenshot, 0.98, 'rectangles')
		# points = vision_gunsnbottle.find(screenshot, 0.7, 'points')

		# debug the loop rate
		print('FPS {}'.format(1 / (time() - loop_time)))
		loop_time = time()

		# press 'q' with the output window focused to exit.
		# waits 1 ms every loop to process key presses
		if cv.waitKey(1) == ord('q'):
			cv.destroyAllWindows()
			break


if __name__ == '__main__':
	overlay_window()

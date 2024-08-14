import os

import cv2 as cv
import pyautogui
from PIL import ImageGrab, Image

from router import DirectoryPaths
from src.config_manager import ConfigManagerMixin
from src.logging_config import logger

script_dir = os.path.dirname(os.path.abspath(__file__))
config_json = os.path.join(script_dir, '..', 'json/config.json')
images_dir = os.path.join(script_dir, '..', 'du_images')

config_manager = ConfigManagerMixin()


def convert_to_32_bit():
	# Set the path to your directory containing PNG files
	directory = r"../temp/"

	# Loop through all files in the directory
	for filename in os.listdir(directory):
		if filename.endswith(".png"):
			# Construct the full file path
			file_path = os.path.join(directory, filename)

			# Open the 24-bit PNG image
			image = Image.open(file_path)
			# Convert it to 32-bit by adding an alpha channel (transparency)
			if image.mode != 'RGBA':
				image = image.convert("RGBA")

				# Save the 32-bit PNG image
				image.save(file_path)
			image.close()


def resize_imshow_window(window_name, width, height):
	cv.namedWindow(window_name, cv.WINDOW_NORMAL)
	cv.resizeWindow(window_name, width, height)


def template_matching(image_to_compare):
	if os.path.exists(image_to_compare):
		logger.debug("File exists")
	else:
		logger.debug("File does not exist")

	screen_w, screen_h = pyautogui.size()
	cell_screenshot = ImageGrab.grab(bbox=(0, 0, screen_w, screen_h))
	# Convert the screenshot to a 32-bit image
	cell_screenshot = cell_screenshot.convert("RGBA")
	path = os.path.join(DirectoryPaths.TEMP_DIR, "template_match_screenshot.png")
	screenshot = path
	cell_screenshot.save(screenshot)
	image1 = screenshot
	# image_data = ImageQuerySet().read_image_by_name(image_name=image_to_compare)
	image_data = image_to_compare
	# image_data = f"..\\{image_to_compare}"

	# Set the path to your directory containing PNG files
	haystack_img = cv.imread(image1, cv.IMREAD_UNCHANGED)

	needle_img = cv.imread(image_data, cv.IMREAD_UNCHANGED)
	try:
		result = cv.matchTemplate(haystack_img, needle_img, cv.TM_CCOEFF_NORMED)
		coords = result.shape[0], result.shape[1]
	except Exception as e:
		print(e)
	else:
		# get the best match position
		min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

		# print("Best match top left position: %s" % str(max_loc))
		# print("Best match confidence: %s" % max_val)

		threshold = 0.75
		if max_val >= threshold:
			print(f"Found needle: {image_data} - {max_val} match | threshold: {threshold}")
			# get dimensions of the needle image
			needle_w = needle_img.shape[1]
			needle_h = needle_img.shape[0]

			top_left = max_loc
			bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)

			# Calculate the center of the matched region
			center_x = int((top_left[0] + bottom_right[0]) / 2)
			center_y = int((top_left[1] + bottom_right[1]) / 2)
			coords = center_x, center_y

			cv.rectangle(
				haystack_img,
				top_left,
				bottom_right,
				color=(0, 255, 0),
				thickness=2,
				lineType=cv.LINE_4,
			)
			resize_imshow_window("window", 900, 600)  # Resize the window to 800x600
			cv.imshow("window", haystack_img)
			cv.waitKey(1)
			return coords

		else:
			print(f"Needle not found: {image_data} - {max_val} match | threshold: {threshold}")

		# resize_imshow_window("window", 900, 600)  # Resize the window to 800x600
		# cv.imshow("window", haystack_img)
		# cv.waitKey(1)
		# return coords


if __name__ == '__main__':
	convert_to_32_bit()
	template_matching(image_to_compare=r"C:\Repositories\Dual Universe\DualUniverse_Projects\MDU\data\images\geforce_screen\geforce_select_game.png")

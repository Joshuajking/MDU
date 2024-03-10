import datetime
import os.path

import cv2
import easyocr
import numpy as np
import pyautogui
from PIL import Image, ImageGrab, ImageEnhance
from pynput.mouse import Controller

from config.config_manager import ConfigManager
from models.models import SearchAreaLocation
from path_router import DirectoryPaths
from querysets.querysets import SearchAreaQuerySet


class ResponseData:
	def __init__(self, success: bool, message: str, text: str | None):
		self.success = success
		self.message = message
		self.text = text


class OCREngine:

	def __init__(self, coords=None):
		self.screen_w, self.screen_h = pyautogui.size()
		self.screen_size = (self.screen_w, self.screen_h)
		self.coords = coords
		self.mouse = None
		self.reader = None
		self.click = None
		self.scroll = None
		self.scrap = None

	def get_mouse(self):
		if self.mouse is None:
			self.mouse = Controller()
		return self.mouse

	def get_reader(self):
		if self.reader is None:
			self.reader = easyocr.Reader(["en"], gpu=True)
		return self.reader

	def image_enhancement(self, image, factors=None):
		if factors:
			# Apply brightness enhancement
			brightness_factor = factors.get("brightness", 1.0)
			brightness = ImageEnhance.Brightness(image).enhance(brightness_factor)
			"""Adjust image brightness.
                This class can be used to control the brightness of an image.  An
                enhancement factor of 0.0 gives a black image. A factor of 1.0 gives the
                original image.
                """

			# Apply sharpness enhancement
			sharpness_factor = factors.get("sharpness", 1.0)
			sharpness = ImageEnhance.Sharpness(brightness).enhance(sharpness_factor)
			"""Adjust image sharpness.
                This class can be used to adjust the sharpness of an image. An
                enhancement factor of 0.0 gives a blurred image, a factor of 1.0 gives the
                original image, and a factor of 2.0 gives a sharpened image.
                """

			# Apply color enhancement
			color_factor = factors.get("color", 1.0)
			color = ImageEnhance.Color(sharpness).enhance(color_factor)
			"""Adjust image color balance.
                This class can be used to adjust the colour balance of an image, in
                a manner similar to the controls on a colour TV set. An enhancement
                factor of 0.0 gives a black and white image. A factor of 1.0 gives
                the original image.
                """

			# Apply contrast enhancement
			contrast_factor = factors.get("contrast", 1.0)
			contrast = ImageEnhance.Contrast(color).enhance(contrast_factor)
			"""Adjust image contrast.
                This class can be used to control the contrast of an image, similar
                to the contrast control on a TV set. An enhancement factor of 0.0
                gives a solid grey image. A factor of 1.0 gives the original image.
                """

			# Convert to grayscale if 'grayscale' flag is True
			if factors.get("grayscale", False):
				grayscale = cv2.cvtColor(np.array(contrast), cv2.COLOR_BGR2GRAY)
				contrast = Image.fromarray(grayscale)

			# Apply Gaussian Blur (if specified)
			# if 'GaussianBlur' in factors:
			if factors.get("GaussianBlur", False):
				ksize = factors["GaussianBlur"].get("ksize", (1, 1))
				sigmaX = factors["GaussianBlur"].get("sigmaX", 0)
				contrast = cv2.GaussianBlur(np.array(contrast), ksize, sigmaX)
				contrast = Image.fromarray(contrast)

			return contrast
		return image

	def convert_screenshot_to_32bit(self, area_screenshot):
		cell_screenshot = area_screenshot.convert("RGBA")
		screenshot = os.path.join(DirectoryPaths.TEMP_DIR, "ocr_screenshot.png")
		cell_screenshot.save(screenshot)
		cell_screenshot.close()

		# Use the temp_file.name for further processing or return it
		return screenshot

	def absolute_coords(self, bounding_box, region):
		# Coordinates of the text/image within the region
		text_x1, text_y1 = bounding_box[0]
		text_x2, text_y2 = bounding_box[2]

		# Coordinates of the region
		region_x1, region_y1, region_x2, region_y2 = [
			region.left,
			region.top,
			region.right,
			region.bottom,
		]

		# Coordinates of the screen
		screen_x1, screen_y1, screen_x2, screen_y2 = [
			0,
			0,
			self.screen_w,
			self.screen_h,
		]

		# Calculate the absolute coordinates of the text/image on the screen
		absolute_x1 = screen_x1 + region_x1 + text_x1
		absolute_y1 = screen_y1 + region_y1 + text_y1
		absolute_x2 = screen_x1 + region_x1 + text_x2
		absolute_y2 = screen_y1 + region_y1 + text_y2

		# Calculate the center point of the bounding box
		center_x = (absolute_x1 + absolute_x2) // 2
		center_y = (absolute_y1 + absolute_y2) // 2
		return center_x, center_y

	def ocr_missions(self, search_area, search_text=None, click=False, scroll=False, scrap=False) -> ResponseData:
		"""

		:param search_area:
		:param search_text:
		:param scroll:
		:param click:
		:param scrap:
		:return: ResponseData(
							success= bool,
							message= str,
							text= str
						)
		"""
		self.click = click
		self.scroll = scroll
		self.scrap = scrap
		region = SearchAreaQuerySet.read_search_area_by_name(
			region_name=search_area
		)

		pyautogui.moveTo(region.center_x, region.center_y)
		if self.scroll:
			pyautogui.moveTo(region.center_x, region.center_y)
			self.get_mouse().scroll(dx=0, dy=20)
		attempts = 0
		max_attempts = 7
		while attempts <= max_attempts:
			# Capture a screenshot of the current cell
			cell_screenshot = ImageGrab.grab(
				bbox=(region.left, region.top, region.right, region.bottom)
			)
			# Convert the screenshot to a 32-bit image
			screenshot = self.convert_screenshot_to_32bit(cell_screenshot)

			original_image = Image.open(screenshot)
			enhancement_factors = {
				"brightness": 0.6,  # Default 1.0
				"sharpness": 1.5,  # Default 1.0
				"color": 1.0,  # Default 1.0
				"contrast": 1.0,  # Default 1.0
				"grayscale": False,
				"GaussianBlur": False,
				"ksize": (1, 1),  # Default 3
				"sigmaX": 0,  # Default 0
			}
			ocr_params = {
				# 'image': enhanced_screenshot,
				"workers": 0,
				"decoder": "beamsearch",
				"beamWidth": 5,
				"width_ths": 0.5,
				"contrast_ths": 0.1,
				"adjust_contrast": 0.5,
				"batch_size": 64,
				"mag_ratio": 1,
			}
			"""
                Text Layout Analysis:
                    paragraph: Set to True to enable paragraph analysis.
                    min_size: Minimum text size to recognize.
                    contrast_ths: Specifies the contrast threshold for text detection.
                Image Preprocessing:
                    text_threshold (float, default = 0.7) - Text confidence threshold
                    low_text (float, default = 0.4) - Text low-bound score
                    link_threshold (float, default = 0.4) - Link confidence threshold
                    canvas_size (int, default = 2560) - Maximum image size. Image bigger than this value will be resized down.
                    mag_ratio (float, default = 1) - Image magnification ratio.
                """
			timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
			enhanced_image = self.image_enhancement(
				original_image, factors=enhancement_factors
			)
			enhanced_screenshot = f"{DirectoryPaths.OCR_ENHANCED_DIR}ocr_enhanced_image_{search_text}_{timestamp}.png"
			enhanced_image.save(enhanced_screenshot)
			enhanced_image.close()

			# if isinstance(search_text, str):
			# 	search_text = [search_text]

			cell_result = self.get_reader().readtext(image=enhanced_screenshot, **ocr_params)
			if self.scrap:
				if cell_result:
					return cell_result[0][1]
				else:
					continue
			for mission, (bounding_box, text, _) in enumerate(cell_result):
				temp_img = search_text.replace("_", " ")
				if temp_img in text:
					ocr_text = temp_img
					center_x, center_y = self.absolute_coords(bounding_box, region)

					pyautogui.moveTo(center_x, center_y)
					if self.click:
						pyautogui.click(center_x, center_y)
					self.coords = center_x, center_y

					return ResponseData(
						success=True,
						message="TEXT_FOUND",
						text=text
					)
			if self.scroll:
				pyautogui.moveTo(region.center_x, region.center_y)
				self.get_mouse().scroll(dx=0, dy=-2)
			attempts += 1
			continue

		return ResponseData(
			success=False,
			message="OCR_MAX_ATTEMPTS_EXCEEDED",
			text=None
		)


if __name__ == '__main__':
	config_manager = ConfigManager()
	active_mission_name = config_manager.get_value('config.active_mission_name')
	ocr = OCREngine()
	ocr_scan = ocr.ocr_missions(
		search_area=SearchAreaLocation.AVAILABLE_MISSIONS,
		search_text=active_mission_name,
		scroll=True,
		click=True
	)

# # Assuming `cell_result` contains OCR results for the bounding box
# # Extracting values to the right of the labels
# reward = None
# reward_per_km = None
# collateral = None
#
# # Loop through each text line in the bounding box
# for _, (bounding_box, text, _) in enumerate(cell_result):
# 	# Split the text into label and value based on the presence of "h"
# 	parts = text.split("h")
# 	if len(parts) == 2:
# 		label = parts[0].strip()
# 		value = parts[1].strip()
#
# 		# Assign values based on the label
# 		if label == "REWARD":
# 			reward = value
# 		elif label == "REWARD PER KM":
# 			reward_per_km = value
# 		elif label == "COLLATERAL":
# 			collateral = value
#
# # Now `reward`, `reward_per_km`, and `collateral` contain the extracted values
# print("REWARD:", reward)
# print("REWARD PER KM:", reward_per_km)
# print("COLLATERAL:", collateral)

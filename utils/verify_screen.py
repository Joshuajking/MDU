import random
from time import sleep
from typing import Union

import pyautogui
import pydirectinput
import pytweening

from logs.logging_config import logger
from querysets.querysets import ImageQuerySet


class VerifyScreen:
	def __init__(self):
		success = False
		self.region_str = None
		self.w, self.h = pyautogui.size()
		self.screen_size = self.w//2, self.h//2
		pass

	def simulate_mouse(self, dest_x, dest_y, mouse_click, mouse_clicks):
		# Get screen size
		screen_width, screen_height = pyautogui.size()
		EASING_FUNCTIONS = {
			# "linear": pytweening.linear,
			"easeInQuad": pytweening.easeInQuad,
			"easeOutQuad": pytweening.easeOutQuad,
			"easeInOutQuad": pytweening.easeInOutQuad,
			"easeInCubic": pytweening.easeInCubic,
			"easeOutCubic": pytweening.easeOutCubic,
			"easeInOutCubic": pytweening.easeInOutCubic,
			"easeInQuart": pytweening.easeInQuart,
			"easeOutQuart": pytweening.easeOutQuart,
			"easeInOutQuart": pytweening.easeInOutQuart,
			"easeInQuint": pytweening.easeInQuint,
			"easeOutQuint": pytweening.easeOutQuint,
			"easeInOutQuint": pytweening.easeInOutQuint,
			"easeInSine": pytweening.easeInSine,
			"easeOutSine": pytweening.easeOutSine,
			"easeInOutSine": pytweening.easeInOutSine,
			"easeInExpo": pytweening.easeInExpo,
			"easeOutExpo": pytweening.easeOutExpo,
			"easeInOutExpo": pytweening.easeInOutExpo,
			"easeInCirc": pytweening.easeInCirc,
			"easeOutCirc": pytweening.easeOutCirc,
			"easeInOutCirc": pytweening.easeInOutCirc,
		}

		# Generate a random key
		easing_key = random.choice(list(EASING_FUNCTIONS.keys()))

		# Get the selected easing function object
		selected_easing_function = EASING_FUNCTIONS[easing_key]

		x = random.randint(-23, 27)
		x += dest_x

		y = random.randint(-32, 44)
		y += dest_y

		pyautogui.moveTo(x, y, duration=random.uniform(0.1, 2.2), tween=selected_easing_function, _pause=True)

		# Use the selected easing function in pyautogui.moveTo
		pyautogui.moveTo(dest_x, dest_y, duration=random.uniform(0.1, 1.2), tween=selected_easing_function, _pause=True)
		if mouse_click:
			# pyautogui.click(clicks=mouse_clicks, duration=random.uniform(0.2, 0.4))
			pydirectinput.click(clicks=mouse_clicks, interval=0.2)
		return

	def screen(
			self,
			screen_name: str = None,
			image_to_compare: str = None,
			confidence: float = 0.8,
			minSearchTime: int = 2,
			mouse_clicks: int = 1,
			verify_screen: bool = False,
			skip_sleep: bool = False,
			mouse_click: bool = False,
			# region: Union[tuple, int] = None,
			esc: bool = False,
	):
		"""
             Verify screen details and return screen coordinates if found.
    
        :param screen_name: str, mandatory - The screen name to VerifyScreen.
        :param image_to_compare: str, mandatory - The image to compare for verification.
        :param confidence: float - The confidence threshold for verification (default: 0.8).
        :param minSearchTime: float - The minimum search time (default: 30).
        :param mouse_clicks: int - The number of mouse clicks to perform (default: 1).
        :param verify_screen: bool - If True, only VerifyScreen the screen without other optional params.
        :param skip_sleep: bool - If True, skip sleep during verification.
        :param esc: bool, optional - If provided, flag to press the 'esc' key during verification.
        :param mouse_click: bool, optional - If provided, perform a mouse click during verification.
        :param region: tuple, optional - The region to search for the screen.
    
        :return: {'success': True, 'screen_coords': screen_coords, 'bbox': (left, top, width, height), 'minSearchTime': minSearchTime} or False return {'success': False, 'screen_coords': None, 'minSearchTime': minSearchTime}
        """
		if skip_sleep:
			minSearchTime = 5
		is_on_screen = False
		check_count = 0
		max_checks = 60

		image_data = ImageQuerySet.read_image_by_name(image_name=image_to_compare, image_location=screen_name)
		region = image_data.region if image_data is not None else None
		if not image_data.image_location == screen_name:
			raise ValueError(
				f"Error: screen passed {screen_name}, but image_location for {image_to_compare} is {image_data.image_location}")
		while max_checks >= check_count:
			if (screen_coords := pyautogui.locateOnScreen(
					image=image_data.image_url,
					region=region,
					minSearchTime=minSearchTime,
					confidence=confidence,
			)) is not None:
				left, top, width, height = screen_coords
				right = left + width
				bottom = top + height
				center_x = left + width // 2
				center_y = top + height // 2
				screen_coords = center_x, center_y

				# Convert tuple to a string representation
				self.region_str = f"({left}, {top}, {width}, {height})"

				# if not image_data.region:
				# 	image_data = ImageQuerySet.update_image_by_id(image_data.id, {
				# 		'left': int(left),
				# 		'top': int(top),
				# 		'right': int(right),
				# 		'bottom': int(bottom),
				# 		'center_x': int(center_x),
				# 		'center_y': int(center_y),
				# 		'region': self.region_str
				# 	})
				if verify_screen:
					pass

				elif skip_sleep and mouse_click is True and not esc:
					x, y, = screen_coords
					self.simulate_mouse(x, y, mouse_click, mouse_clicks)
					pass

				elif mouse_click is True and not skip_sleep and not esc:
					x, y, = screen_coords
					self.simulate_mouse(x, y, mouse_click, mouse_clicks)
					pass

				elif mouse_click is True and skip_sleep and esc:
					x, y, = screen_coords
					self.simulate_mouse(x, y, mouse_click, mouse_clicks)
					pass

				elif skip_sleep:
					pass

			elif skip_sleep and esc:
				pydirectinput.press("esc")
				check_count += 1
				continue

			elif skip_sleep:
				pass

			else:
				check_count += 1
				logger.info(f"looking... {image_to_compare}, {screen_name} {check_count}/{max_checks}")
				continue

			sleep(random.uniform(0.10, 1.0))
			if screen_coords is None:
				return {
				    'success': False,
				    'screen_coords': screen_coords,
				    'minSearchTime': minSearchTime,
				}
			else:
				return {
					'success': True,
					'screen_coords': screen_coords,
					'minSearchTime': minSearchTime,
				}
		logger.error(
			{
				"screen_name": screen_name,
				"image_to_compare": image_to_compare,
				"confidence": confidence,
				"minSearchTime": minSearchTime,
				"mouse_clicks": mouse_clicks,
				"verify_screen": verify_screen,
				"skip_sleep": skip_sleep,
				"mouse_click": mouse_click,
				"region": region,
				"esc": esc,
				"screen_coords": screen_coords,
			}
		)
		raise TimeoutError(f'Timed out waiting for {image_to_compare}')


if __name__ == "__main__":
	# self.verify.screen("test", "agg_hold", skip_sleep=True)
	pass
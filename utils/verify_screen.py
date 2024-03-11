import random
from time import sleep
from typing import Union

import pyautogui
import pydirectinput
from loguru import logger
from querysets.querysets import ImageQuerySet


class VerifyScreen:
	def __init__(self):
		success = False
		self.region_str = None
		pass

	def screen(
			self,
			screen_name: str = None,
			image_to_compare: str = None,
			confidence: float = 0.8,
			minSearchTime: int = 2,
			mouse_clicks: int = 1,
			verify_screen: bool = False,
			skip_sleep: bool = False,
			mouse_click: int = 0,
			region: Union[tuple, int] = None,
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
		max_checks = 30

		image_data = ImageQuerySet.read_image_by_name(image_name=image_to_compare, image_location=screen_name)
		if not image_data.image_location == screen_name:
			raise ValueError(
				f"Error: screen passed {screen_name}, but image_location for {image_to_compare} is {image_data.image_location}")
		while max_checks >= check_count:
			screen_coords = pyautogui.locateOnScreen(
				image=image_data.image_url,
				region=region,
				minSearchTime=minSearchTime,
				confidence=confidence,
			)

			if screen_coords is not None:
				left, top, width, height = screen_coords
				right = left + width
				bottom = top + height
				center_x = left + width // 2
				center_y = top + height // 2
				screen_coords = center_x, center_y

				# Convert tuple to a string representation
				self.region_str = f"({left}, {top}, {width}, {height})"

				if not image_data.region:
					image_data = ImageQuerySet.update_image_by_id(image_data.id, {
						'left': int(left),
						'top': int(top),
						'right': int(right),
						'bottom': int(bottom),
						'center_x': int(center_x),
						'center_y': int(center_y),
						'region': self.region_str
					})
				if verify_screen:
					pass

				elif skip_sleep and mouse_click == 1 and not esc:
					pyautogui.click(screen_coords, clicks=mouse_clicks)
					pass

				elif mouse_click == 1 and not skip_sleep and not esc:
					pyautogui.click(screen_coords, clicks=mouse_clicks)
					pass

				elif mouse_click == 1 and skip_sleep and esc:
					pyautogui.click(screen_coords, clicks=mouse_clicks)
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
				"region": self.region_str,
				"esc": esc,
				"screen_coords": screen_coords,
			}
		)
		raise TimeoutError(f'Timed out waiting for {image_to_compare}')


if __name__ == "__main__":
	# self.verify.screen("test", "agg_hold", skip_sleep=True)
	pass
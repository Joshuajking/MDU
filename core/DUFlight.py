from time import sleep, perf_counter

import pyautogui
import pydirectinput
from logs.logging_config import logger

from config.config_manager import ConfigManager
from models.models import ImageLocation
from querysets.querysets import ImageQuerySet, CharacterQuerySet
from utils.special_mission_ocr import OCREngine
from utils.verify_screen import VerifyScreen


class DUFlight:

	def __init__(self):
		self.config_manager = ConfigManager()
		self.verify = VerifyScreen()
		self.ocr = OCREngine()
		self.character = CharacterQuerySet.read_character_by_username(self.config_manager.get_value('config.pilot'))
		self.flight_images = ImageQuerySet.get_all_image_by_location(image_location=ImageLocation.FLIGHT_SCREEN)

	def cytt_hq(self):
		attempts = 60
		count = 0

		while count <= attempts:
			verify_response = self.verify.screen(
				screen_name=ImageLocation.FLIGHT_SCREEN,
				image_to_compare="origin_sicari",
				confidence=0.8,
				skip_sleep=True,
			)

			if verify_response['screen_coords'] is not None:
				pydirectinput.keyDown("alt")
				pydirectinput.press("4")
				sleep(0.5)
				pydirectinput.keyUp("alt")
				sleep(0.25)
				pydirectinput.press("ctrl")
				pydirectinput.middleClick()
				self.check_img_to_land()
				pydirectinput.keyDown("f")
				sleep(4)
				pydirectinput.keyUp("f")
				return
			else:
				pydirectinput.keyDown("alt")
				pydirectinput.press("2")
				pydirectinput.keyUp("alt")
				count += 1
			return

	def mission_flight(self, retrieve_mode):
		self.respawn()

		sleep(0.5)
		pydirectinput.keyDown("f")
		sleep(4)
		pydirectinput.keyUp("f")

		if retrieve_mode:
			image_to_compare = self.config_manager.get_value("config.mission_retrieve_loc")
		else:
			image_to_compare = self.config_manager.get_value("config.mission_delivery_loc")

		attempts = 60
		count = 0
		while count <= attempts:

			response_image_to_compare = self.verify.screen(
				screen_name=ImageLocation.FLIGHT_SCREEN,
				image_to_compare=image_to_compare,
				skip_sleep=True
			)

			if response_image_to_compare['screen_coords'] is not None:
				pydirectinput.keyDown("alt")
				pydirectinput.press("4")
				sleep(0.5)
				pydirectinput.keyUp("alt")
				sleep(0.25)
				pydirectinput.press("ctrl")
				pydirectinput.middleClick()
				flight_time_start = perf_counter()
				self.check_img_to_land()
				flight_time_stop = perf_counter()
				tt_flight_time = flight_time_stop - flight_time_start
				logger.info(f"flightTime: {flight_time_stop - flight_time_start}")
				pydirectinput.keyDown("f")
				sleep(4)
				pydirectinput.keyUp("f")
				return tt_flight_time
			else:
				pydirectinput.keyDown("alt")
				pydirectinput.press("2")
				pydirectinput.keyUp("alt")
				count += 1
				continue
		return

	def check_img_to_land(self):
		sleep(10)
		logger.info(f"waiting to land...")

		time_in_flight = 0
		max_flight_time = 1200
		screen_coords = None

		while screen_coords is None or time_in_flight <= max_flight_time:
			screen_coords = pyautogui.locateCenterOnScreen(
				image=r"C:\Repositories\Dual Universe\Missions Dual Universe\data\search_areas\ORBITAL_HUD_LANDED.png",
				minSearchTime=1,
				confidence=0.8,
			)

			if screen_coords is not None:
				break

			time_in_flight += 1

		# Gives time for the ship to land before continuing
		sleep(20)
		return
	# def check_img_to_land(self):
	# 	sleep(10)
	# 	logger.info(f"waiting to land...")
	#
	# 	time_in_flight = 0
	# 	max_flight_time = 400
	# 	screen_coords = None
	#
	# 	# Use tqdm as a progress bar
	# 	for _ in tqdm(range(max_flight_time), desc="Searching for landing image", file=sys.stdout):
	# 		screen_coords = pyautogui.locateCenterOnScreen(
	# 			image=r"C:\Repositories\Dual Universe\Missions Dual Universe\data\search_areas\ORBITAL_HUD_LANDED.png",
	# 			minSearchTime=3,
	# 			confidence=0.8,
	# 		)
	#
	# 		if screen_coords is not None:
	# 			break
	#
	# 		time.sleep(1)  # Adjust sleep time if needed
	#
	# 	# Gives time for the ship to land before continuing
	# 	sleep(20)
	# 	return

	def respawn(self):
		sleep(1)
		pydirectinput.press("esc")
		respawn_btn = self.verify.screen(
			screen_name=ImageLocation.LOGOUT_SCREEN,
			image_to_compare="respawn_btn",
			skip_sleep=True,
			esc=True,
			mouse_click=1
		)

		respawn_yes_btn = self.verify.screen(
			screen_name=ImageLocation.LOGOUT_SCREEN,
			image_to_compare="respawn_confirmation_btn",
			mouse_click=1
		)
		respawn_ok = self.verify.screen(
			screen_name=ImageLocation.IN_GAME_SCREEN,
			image_to_compare="selected_ok_btn",
			mouse_click=1
		)
		return


if __name__ == "__main__":
	obj = DUFlight()
	obj.check_img_to_land()

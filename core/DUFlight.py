import time
from time import sleep, perf_counter

import pyautogui
import pydirectinput

from config.config_manager import ConfigManager, timing_decorator
from logs.logging_config import logger
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

	@timing_decorator
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
				continue

	@timing_decorator
	def check_img_to_land(self):
		sleep(10)
		logger.info(f"waiting to land...")

		time_in_flight = 0
		timeout_seconds = 1200
		start_time = time.perf_counter()
		screen_coords = None

		while screen_coords is None:
			screen_coords = pyautogui.locateCenterOnScreen(
				image=r"C:\Repositories\Dual Universe\Missions Dual Universe\data\search_areas\ORBITAL_HUD_LANDED.png",
				minSearchTime=1,
				confidence=0.8,
			)
			elapsed_time = time.perf_counter() - start_time
			if elapsed_time >= timeout_seconds:
				break
			sleep(3)
		# Gives time for the ship to land before continuing
		sleep(20)
		return

	@timing_decorator
	def respawn(self):
		sleep(1)
		pydirectinput.press("esc")
		respawn_btn = self.verify.screen(
			screen_name=ImageLocation.LOGOUT_SCREEN,
			image_to_compare="respawn_btn",
			skip_sleep=True,
			esc=True,
			mouse_click=True,
		)

		respawn_yes_btn = self.verify.screen(
			screen_name=ImageLocation.LOGOUT_SCREEN,
			image_to_compare="respawn_confirmation_btn",
			mouse_click=True
		)
		respawn_ok = self.verify.screen(
			screen_name=ImageLocation.IN_GAME_SCREEN,
			image_to_compare="selected_ok_btn",
			mouse_click=True,
			mouse_clicks=2
		)


if __name__ == "__main__":
	obj = DUFlight()
	obj.check_img_to_land()

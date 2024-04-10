import os.path
import time
from time import sleep

import pyautogui
import pydirectinput
from pynput.mouse import Controller

from router import DirectoryPaths
from src.config_manager import ConfigManager, timing_decorator
from src.logging_config import logger
from src.models import ImageLocation
from src.querysets import ImageQuerySet, CharacterQuerySet
from src.special_mission_ocr import OCREngine
from src.verify_screen import VerifyScreen


class PilotSeatNotFoundError(Exception):
	""" PilotSeatNotFound. """

	def __init__(self, message=None, errors=None):
		# Call the base class constructor with the parameters it needs
		super().__init__(message)


class DUFlight:

	def __init__(self):
		self.config_manager = ConfigManager()
		self.verify = VerifyScreen()
		self.ocr = OCREngine()
		self.controller = Controller()
		self.character = CharacterQuerySet.read_character_by_username(self.config_manager.get_value('config.pilot'))
		self.flight_images = ImageQuerySet.get_all_image_by_location(image_location=ImageLocation.FLIGHT_SCREEN)

	def get_pilot_seat(self):
		sleep(0.5)
		pydirectinput.keyDown("f")
		sleep(4)
		pydirectinput.keyUp("f")

	# image_list = ["pilot_seat_lable", "pilot_seat"]
	# for image_name in image_list:
	# 	pilot = self.verify.screen(
	# 		screen_name=ImageLocation.IN_GAME_SCREEN,
	# 		image_to_compare=image_name,
	# 		skip_sleep=True,
	# 	)
	# 	if pilot.get('success'):
	# 		sleep(0.5)
	# 		pydirectinput.keyDown("f")
	# 		sleep(4)
	# 		pydirectinput.keyUp("f")
	# 		return
	# raise PilotSeatNotFoundError(f"Pilot seat not found: {image_name}")
	@timing_decorator
	def get_fuel_level(self):
		timeout_seconds = 14800
		start_time = time.perf_counter()
		fuel_success = True  # Start with True to enter the loop
		while fuel_success:
			fuel_level = self.verify.screen(
				screen_name=ImageLocation.FLIGHT_SCREEN,
				image_to_compare="atmo_fuel_20",
				confidence=0.70,
				skip_sleep=True
			)
			fuel_success = fuel_level['success']
			elapsed_time = time.perf_counter() - start_time
			if elapsed_time >= timeout_seconds:
				logger.debug(f"Fuel level: Timeo-out")
				break

	@timing_decorator
	def flight_locations(self, retrieve_mode):
		# pre_sites = ImageQuerySet.read_image_by_name(
		# 	image_name="pre_site_origin",
		# 	image_location=ImageLocation.FLIGHT_SCREEN) if retrieve_mode else \
		# 	ImageQuerySet.read_image_by_name(
		# 		image_name="pre_site_dest", image_location=ImageLocation.FLIGHT_SCREEN)
		#
		# pre_site = pre_sites.image_name

		image_to_compare = self.config_manager.get_value(
			"config.mission_retrieve_loc") if retrieve_mode else self.config_manager.get_value(
			"config.mission_delivery_loc")

		if retrieve_mode:
			images = [image_to_compare]
			# images = [pre_site, image_to_compare]
			return image_to_compare
		else:
			images = [image_to_compare]
			return image_to_compare

	@timing_decorator
	def mission_flight(self, retrieve_mode):
		self.respawn()
		self.get_pilot_seat()
		# self.get_fuel_level()

		images = self.flight_locations(retrieve_mode)

		# for image in images:
		attempts = 60
		count = 0
		while count < attempts:
			logger.info(f"Looking for image {images}")
			response_image_to_compare = self.verify.screen(
				screen_name=ImageLocation.FLIGHT_SCREEN,
				image_to_compare=images,
				skip_sleep=True
			)
			if response_image_to_compare['screen_coords'] is not None:
				logger.info(f"Procceding to {images} location")
				pydirectinput.keyDown("alt")
				pydirectinput.press("4")
				sleep(0.1)
				pydirectinput.keyUp("alt")
				sleep(20)
				pydirectinput.press("ctrl")
				sleep(0.5)
				pydirectinput.middleClick()
				# self.controller.scroll(dx=0, dy=240)
				self.check_img_to_land()
				break
			else:
				pydirectinput.keyDown("alt")
				pydirectinput.press("2")
				pydirectinput.keyUp("alt")
				count += 1
		else:
			# If no match found after all attempts
			logger.error("No match found for image:", images)
		self.get_pilot_seat()

	def check_ship_landed(self, img=(os.path.join(DirectoryPaths.SEARCH_AREA_DIR, 'ORBITAL_HUD_LANDED.png'))):
		return pyautogui.locateCenterOnScreen(
			image=img,
			minSearchTime=1,
			confidence=0.75,
		)

	def afk_timer(self, afk_start):
		elapsed_time = time.perf_counter() - afk_start
		if elapsed_time >= 900:
			pyautogui.press('tab', presses=2, interval=0.2)
		elif elapsed_time >= 600:
			pyautogui.press('tab', presses=2, interval=0.2)
		elif elapsed_time >= 300:
			pyautogui.press('tab', presses=2, interval=0.2)

	@timing_decorator
	def check_img_to_land(self):
		sleep(10)
		logger.info(f"waiting to land...")

		timeout_seconds = 900
		afk_start = time.perf_counter()
		start_time = time.perf_counter()
		screen_coords = None

		while screen_coords is None:
			screen_coords = self.check_ship_landed()
			elapsed_time = time.perf_counter() - start_time
			self.afk_timer(afk_start)
			if elapsed_time >= timeout_seconds:
				logger.debug(f"check_img_to_land: Timeo-out")
				break
			sleep(3)
		# Gives time for the ship to land before continuing
		sleep(20)
		return

	@timing_decorator
	def respawn(self):
		logger.info(f"Sleeping for 30 seconds while game loads before respawn")
		sleep(30)
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
	# pre_load.load_image_entries_to_db()
	obj = DUFlight()
	obj.get_fuel_level()

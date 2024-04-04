import random
from time import sleep

import pyautogui
import pydirectinput
from ahk import AHK

from config.config_manager import timing_decorator
from logs.logging_config import logger
from model.models import ImageLocation
from querysets.querysets import CharacterQuerySet
from utils.verify_screen import VerifyScreen


class DUCharacters:
	ahk = AHK()

	def __init__(self):
		self.verify = VerifyScreen()

	@timing_decorator
	def login(self, character):

		response_du_login_screen_label = self.verify.screen(
			screen_name=ImageLocation.LOGIN_SCREEN,
			image_to_compare="du_login_screen_label",
			skip_sleep=True,
		)
		if not response_du_login_screen_label['success']:
			self.logout()
		response_du_login_screen_label = self.verify.screen(
			screen_name=ImageLocation.LOGIN_SCREEN,
			image_to_compare="du_login_screen_label",
			# mouse_click=True,
			# mouse_clicks=2
		)
		if not response_du_login_screen_label['success']:
			raise Exception(f"screen not found")
		attempts = 3
		count = 0
		while count <= attempts:
			logger.info(f"logging into {character.username}")

			pydirectinput.press("tab")
			pydirectinput.press("backspace")
			pydirectinput.press("tab")
			pydirectinput.press("backspace")

			response_email_login = self.verify.screen(
				screen_name=ImageLocation.LOGIN_SCREEN,
				image_to_compare="email_login",
				mouse_click=True,
				mouse_clicks=2
			)

			self.ahk.send_raw(character.email)
			sleep(0.2)
			pydirectinput.press("tab")

			response_password_login = self.verify.screen(
				screen_name=ImageLocation.LOGIN_SCREEN,
				image_to_compare="password_login",
				mouse_click=True,
				mouse_clicks=2
			)

			self.ahk.send_raw(character.password)
			sleep(random.uniform(0.1, 0.4))
			pydirectinput.press("enter")

			internal_error = self.verify.screen(
				screen_name=ImageLocation.LOGIN_SCREEN,
				image_to_compare="internal_error",
				confidence=0.8,
				minSearchTime=2,
				skip_sleep=True,
			)
			response_email_login = self.verify.screen(
				screen_name=ImageLocation.LOGIN_SCREEN,
				image_to_compare="email_login",
				mouse_click=True,
				minSearchTime=2,
				skip_sleep=True
			)

			if internal_error['success'] and not response_email_login['success']:
				logger.warning({"success": False, "status": "email_field: failed"})
				continue

			response_gametime_error_lable = self.verify.screen(
				screen_name=ImageLocation.LOGIN_SCREEN,
				image_to_compare="gametime_error_lable",
				skip_sleep=True,
			)

			if response_gametime_error_lable['success']:
				logger.debug(f"No game time: {character.username}")
				CharacterQuerySet.update_character(character, {'has_gametime': False, 'active': False})

				return False

			response_loading_complete = self.verify.screen(
				screen_name=ImageLocation.IN_GAME_SCREEN,
				image_to_compare="loading_complete",

			)

			logger.success(f"{character.username} Successfully loaded game")
			CharacterQuerySet.update_character(character, {'has_gametime': True})
			self.survey()
			self.welcome_reward()
			return True

	@timing_decorator
	def logout(self, respawn=False):

		loading_complete_response = self.verify.screen(
			screen_name=ImageLocation.IN_GAME_SCREEN,
			image_to_compare="loading_complete",
			skip_sleep=True
		)
		if not loading_complete_response['success']:
			return

		count = 0
		max_count = 20
		at_esc_menu = False
		while not at_esc_menu:
			if count >= max_count:
				break

			# pydirectinput.press("esc")
			# sleep(random.uniform(0.5, 2.0))
			logout_btn_response = self.verify.screen(
				screen_name=ImageLocation.LOGOUT_SCREEN,
				image_to_compare="logout_btn",
				skip_sleep=True,
				esc=True,
				mouse_click=True,
				mouse_clicks=1,
			)
			if not logout_btn_response['success']:
				count += 1
				continue
			elif logout_btn_response['success'] and respawn:
				return
			at_esc_menu = True
			# pyautogui.click(logout_btn_response['screen_coords'])
			return

		logger.error({"success": False, "message": "ESC Menu Not Found"})
		raise Exception("ESC Menu Not Found")

	def check_location(self):  # TODO: Implement
		"""Comes in after welcome back reward"""
		step_scroll = 1000
		# Press F4(map)
		pydirectinput.press("f4")
		# wait for map loading
		my_marker = self.verify.screen(screen_name=ImageLocation.MAP_SCREEN, image_to_compare="my_map_marker", confidence=0.8)
		# scroll-in(zoom)
		pyautogui.scroll(step_scroll, my_marker)
		# find planet info
		planet_label = self.verify.screen(
			screen_name=ImageLocation.MAP_SCREEN, image_to_compare="map_planet_label", confidence=0.8,
		)
		# find Market icon
		market_icon = self.verify.screen(screen_name=ImageLocation.MAP_SCREEN, image_to_compare="map_market_icon", confidence=0.8)
		# VerifyScreen Market location
		market_label = self.verify.screen(
			screen_name=ImageLocation.MAP_SCREEN, image_to_compare="map_market_label", confidence=0.8,
		)
		# close map (Esc)
		pydirectinput.press("esc")

	@timing_decorator
	def survey(self):
		survey = self.verify.screen(
			screen_name=ImageLocation.IN_GAME_SCREEN, image_to_compare="survey", skip_sleep=True
		)
		if survey['screen_coords'] is not None:
			self.verify.screen(
				screen_name=ImageLocation.IN_GAME_SCREEN,
				image_to_compare="survey_skip_btn",
				skip_sleep=True,
				mouse_click=True
			)
		return

	@timing_decorator
	def welcome_reward(self):
		"""Checks for Daily reward"""
		welcome_screen = self.verify.screen(
			screen_name=ImageLocation.IN_GAME_SCREEN, image_to_compare="quanta_lable", skip_sleep=True
		)
		if welcome_screen['screen_coords'] is not None:
			self.verify.screen(
				screen_name=ImageLocation.IN_GAME_SCREEN,
				image_to_compare="selected_ok_btn",
				skip_sleep=True,
				mouse_click=True
			)
		return


if __name__ == "__main__":
	obj = DUCharacters()
	obj.logout(respawn=False)

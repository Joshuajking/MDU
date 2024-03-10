from time import sleep

import keyboard
import pyautogui
import pydirectinput
from loguru import logger
from models.models import ImageLocation
from querysets.querysets import CharacterQuerySet
from utils.verify_screen import VerifyScreen


class DUCharacters:
	def __init__(self):
		self.verify = VerifyScreen()
		pass

	def login(self, character):

		sleep(3)
		response_du_login_screen_label = self.verify.screen(
			screen_name=ImageLocation.LOGIN_SCREEN,
			image_to_compare="du_login_screen_label",
			skip_sleep=True,
		)
		if not response_du_login_screen_label['success']:
			self.logout()
			# todo: might need to logout here and get the first() character with has_package = 0 depending on retrieve_status
		response_du_login_screen_label = self.verify.screen(
			screen_name=ImageLocation.LOGIN_SCREEN,
			image_to_compare="du_login_screen_label",
			mouse_click=True,
			mouse_clicks=2
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
				mouse_click=1,
				region=(155, 358, 480, 574)
			)

			keyboard.write(character.email)
			pydirectinput.press("tab")

			response_password_login = self.verify.screen(
				screen_name=ImageLocation.LOGIN_SCREEN,
				image_to_compare="password_login",
				mouse_click=1, region=(155, 358, 480, 574)
			)

			keyboard.write(character.password)

			response_email_login = self.verify.screen(
				screen_name=ImageLocation.LOGIN_SCREEN,
				image_to_compare="email_login",
				confidence=0.8,
				skip_sleep=True,
			)

			if response_email_login['screen_coords'] is not None:
				logger.debug({"success": False, "status": "email_field: failed"})
				continue

			pydirectinput.press("enter")

			response_gametime_error_lable = self.verify.screen(
				screen_name=ImageLocation.LOGIN_SCREEN,
				image_to_compare="gametime_error_lable",
				region=(160, 686, 500, 770),
				skip_sleep=True,
			)

			if response_gametime_error_lable['screen_coords'] is not None:
				logger.warning(f"No game time: {character.username}")
				CharacterQuerySet.update_character(character.id, {'has_gametime': False, 'active': False})

				return False

			response_loading_complete = self.verify.screen(
				screen_name=ImageLocation.IN_GAME_SCREEN,
				image_to_compare="loading_complete",

			)

			logger.success(f"{character.username} Successfully loaded game")
			CharacterQuerySet.update_character(character.id, {'has_gametime': True})
			self.welcome_reward()
			return True

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

			pydirectinput.press("esc")

			logout_btn_response = self.verify.screen(
				screen_name=ImageLocation.LOGOUT_SCREEN,
				image_to_compare="logout_btn",
				skip_sleep=True
			)
			if not logout_btn_response['success']:
				count += 1
				continue
			elif logout_btn_response['success'] and respawn:
				return
			at_esc_menu = True
			pyautogui.click(logout_btn_response['screen_coords'])
			return

		logger.critical({"success": False, "message": "ESC Menu Not Found"})
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
			region=(1457, 135, 1561, 159)
		)
		# find Market icon
		market_icon = self.verify.screen(screen_name=ImageLocation.MAP_SCREEN, image_to_compare="map_market_icon", confidence=0.8)
		# VerifyScreen Market location
		market_label = self.verify.screen(
			screen_name=ImageLocation.MAP_SCREEN, image_to_compare="map_market_label", confidence=0.8,
			region=(432, 607, 685, 640)
		)
		# close map (Esc)
		pydirectinput.press("esc")

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
				mouse_click=1
			)
		return


if __name__ == "__main__":
	obj = DUCharacters()
	obj.logout(respawn=False)

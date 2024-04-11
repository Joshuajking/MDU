import multiprocessing
import random
from time import sleep

import pyautogui
import pydirectinput
from ahk import AHK

from src.config_manager import timing_decorator
from src.logging_config import logger
from src.models import ImageLocation
from src.querysets import CharacterQuerySet
from src.verify_screen import VerifyScreen


def get_du_login_screen_label(verify):
	result = verify.screen(
		screen_name=ImageLocation.LOGIN_SCREEN,
		image_to_compare="du_login_screen_label",
		skip_sleep=True,
	)
	return result['success'], result['screen_coords'], result['minSearchTime']


def get_loading_complete(verify):
	result = verify.screen(
		screen_name=ImageLocation.IN_GAME_SCREEN,
		image_to_compare="loading_complete",
		skip_sleep=True,
	)
	return result['success'], result['screen_coords'], result['minSearchTime']


def get_connection_queued(verify):
	result = verify.screen(
		screen_name=ImageLocation.LOGIN_SCREEN,
		image_to_compare="connection_queued",
		confidence=0.8,
		minSearchTime=2,
		skip_sleep=True,
	)
	return result['success'], result['screen_coords'], result['minSearchTime']


def get_internal_error(verify):
	result = verify.screen(
		screen_name=ImageLocation.LOGIN_SCREEN,
		image_to_compare="internal_error",
		confidence=0.8,
		minSearchTime=2,
		skip_sleep=True,
	)
	return result['success'], result['screen_coords'], result['minSearchTime']


def get_email_login(verify):
	result = verify.screen(
		screen_name=ImageLocation.LOGIN_SCREEN,
		image_to_compare="email_login",
		confidence=0.8,
		minSearchTime=2,
		skip_sleep=True,
	)
	return result['success'], result['screen_coords'], result['minSearchTime']


def get_gametime_error_lable(verify):
	result = verify.screen(
		screen_name=ImageLocation.LOGIN_SCREEN,
		image_to_compare="gametime_error_lable",
		confidence=0.8,
		minSearchTime=2,
		skip_sleep=True,
	)
	return result['success'], result['screen_coords'], result['minSearchTime']


def get_password_error(verify):
	result = verify.screen(
		screen_name=ImageLocation.LOGIN_SCREEN,
		image_to_compare="password_error_lable",
		confidence=0.8,
		minSearchTime=2,
		skip_sleep=True,
	)
	return result['success'], result['screen_coords'], result['minSearchTime']


class DUCharacters:

	def __init__(self):
		self.ahk = AHK()
		self.verify = VerifyScreen()

	@timing_decorator
	def login(self, character):

		with multiprocessing.Pool(processes=2) as pool:
			du_login_screen_label_result = pool.apply_async(get_du_login_screen_label, (self.verify,))
			loading_complete_result = pool.apply_async(get_loading_complete, (self.verify,))

			success_du_login_screen_label, screen_coords_du_login_screen_label, minSearchTime_du_login_screen_label = du_login_screen_label_result.get()
			success_loading_complete, screen_coords_loading_complete, minSearchTime_loading_complete = loading_complete_result.get()

			if not success_du_login_screen_label:
				self.logout()
			elif not success_loading_complete:
				pass
			elif not success_du_login_screen_label and success_loading_complete:
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
			if not response_email_login['success']:
				continue

			self.ahk.send_raw(character.email)
			sleep(0.2)
			pydirectinput.press("tab")

			response_password_login = self.verify.screen(
				screen_name=ImageLocation.LOGIN_SCREEN,
				image_to_compare="password_login",
				mouse_click=True,
				mouse_clicks=2
			)
			if not response_password_login['success']:
				continue

			self.ahk.send_raw(character.password)
			sleep(random.uniform(0.1, 0.4))
			pydirectinput.press("enter")

			with multiprocessing.Pool(processes=5) as pool:
				connection_queued_result = pool.apply_async(get_connection_queued, (self.verify,))
				# email_login_result = pool.apply_async(get_email_login, (self.verify,))
				internal_error_result = pool.apply_async(get_internal_error, (self.verify,))
				gametime_error_lable_result = pool.apply_async(get_gametime_error_lable, (self.verify,))
				password_error_result = pool.apply_async(get_password_error, (self.verify,))

				success_connection_queued, screen_coords_connection_queued, minSearchTime_connection_queued = connection_queued_result.get()
				# success_email_login, screen_coords_email_login, minSearchTime_email_login = email_login_result.get()
				success_internal_error, screen_coords_internal_error, minSearchTime_internal_error = internal_error_result.get()
				success_gametime_error_lable, screen_coords_gametime_error_lable, minSearchTime_gametime_error_lable = gametime_error_lable_result.get()
				success_password_error, screen_coords_password_error, minSearchTime_password_error = password_error_result.get()

			if success_internal_error:
				logger.warning(f"Internal error: Server not responding")
				continue
			elif success_gametime_error_lable:
				CharacterQuerySet.update_character(character, {'has_gametime': False, 'active': False})
				logger.warning(f"Gametime error: {character.email} deactivated")
				return False
			elif success_password_error:
				CharacterQuerySet.update_character(character, {'has_gametime': False, 'active': False})
				logger.warning(f"Password error: character {character.email} deactivated")
				return False
			# elif success_email_login:
			# 	logger.warning(f"Email error: {character.email} was skipped")
			# 	continue
			elif success_connection_queued:
				CharacterQuerySet.update_character(character, {'has_gametime': True})
				logger.success(f"Connection successful: character {character.email} active")

			response_loading_complete = self.verify.screen(
				screen_name=ImageLocation.IN_GAME_SCREEN,
				image_to_compare="loading_complete",

			)
			self.survey()
			self.welcome_reward()
			return True
		logger.error(f"Error occured: loop timed out")
		raise Exception(f"Error occured: loop timed out")

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
			sleep(random.uniform(0.75, 1.5))
			logout_btn_response = self.verify.screen(
				screen_name=ImageLocation.LOGOUT_SCREEN,
				image_to_compare="logout_btn",
				skip_sleep=True,
				esc=True,
				mouse_click=True,
				mouse_clicks=2,
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
		my_marker = self.verify.screen(screen_name=ImageLocation.MAP_SCREEN, image_to_compare="my_map_marker",
		                               confidence=0.8)
		# scroll-in(zoom)
		pyautogui.scroll(step_scroll, my_marker)
		# find planet info
		planet_label = self.verify.screen(
			screen_name=ImageLocation.MAP_SCREEN, image_to_compare="map_planet_label", confidence=0.8,
		)
		# find Market icon
		market_icon = self.verify.screen(screen_name=ImageLocation.MAP_SCREEN, image_to_compare="map_market_icon",
		                                 confidence=0.8)
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
	all_active_characters = CharacterQuerySet.get_active_characters()
	for character in all_active_characters:
		obj.login(character)
	obj.logout(respawn=False)

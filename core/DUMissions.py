from time import sleep

import pydirectinput
import pyperclip
from logs.logging_config import logger

from config.config_manager import ConfigManager
from models.models import SearchAreaLocation, ImageLocation
from querysets.querysets import CharacterQuerySet, SearchAreaQuerySet
from utils.special_mission_ocr import OCREngine
from utils.verify_screen import VerifyScreen


class DUMissions:
	def __init__(self):
		self.config_manager = ConfigManager()
		self.ocr = OCREngine()
		self.active_mission_name = self.config_manager.get_value(
			"config.active_mission_name"
		)
		self.verify = VerifyScreen()

	def get_package_coords(self):
		orign = SearchAreaQuerySet.get_searcharea_by_name(name=SearchAreaLocation.ORIGIN_POS)

		origin_coords = self.verify.screen(
			screen_name=ImageLocation.MISSION_DETAILS_SCREEN,
			image_to_compare="copy_coords",
			confidence=0.8,
			# region=orign,
			mouse_click=1,
		)

		origin_pos = pyperclip.paste()
		print(origin_pos)

		dest_coords = self.verify.screen(
			screen_name=ImageLocation.MISSION_DETAILS_SCREEN,
			image_to_compare="copy_coords",
			confidence=0.8,
			region=(1457, 605, 1521, 654),
			mouse_click=1,
		)

		dest_pos = pyperclip.paste()

		# title = self.active_mission_name
		# mission = MissionQuerySet.update_mission(title, {
		# 	"origin_pos": origin_pos,
		# 	"destination_pos": dest_pos,
		# })

		return origin_pos, dest_pos

	def ocr_RETRIEVE_DELIVERY_STATUS(self):
		search_text_list = ["RETRIEVE PACKAGE", "DELIVER PACKAGE"]
		for text in search_text_list:
			mission_package_btn = self.ocr.ocr_missions(
				search_area=SearchAreaLocation.RETRIEVE_DELIVERY_STATUS,
				search_text=text,
			)

			if mission_package_btn.text == "RETRIEVE PACKAGE":
				return {"has_package": False}
			elif mission_package_btn.text == "DELIVER PACKAGE":
				return {"has_package": True}
		logger.error(f"{search_text_list} could not be found")
		raise ValueError()

	def process_package(self, character, is_retrieve):
		screen_name = ImageLocation.RETRIEVE_DELIVER_DETAILS_SCREEN
		image_to_compare = "selected_deliver_pkg_btn" if is_retrieve else "selected_retrieve_pkg_btn"
		action = "Delivered" if is_retrieve else "Retrieved"

		result = self.verify.screen(
			screen_name=screen_name,
			image_to_compare=image_to_compare,
			mouse_click=1,
			skip_sleep=True,
		)

		if result['success']:
			# CharacterQuerySet.update_character(character.id, {'has_package': not is_retrieve})
			logger.info(f"{character.username} {action} a package")
			return {"has_package": not is_retrieve}
		else:
			return self.ocr_RETRIEVE_DELIVERY_STATUS()

	def deliver_package(self, character):
		pydirectinput.press("f8")
		is_active_mission = self.ocr.ocr_missions(
			search_area=SearchAreaLocation.ACTIVE_TAKEN_MISSIONS,
			search_text=self.active_mission_name,
			click=True,
		)

		if is_active_mission.success:
			result = self.verify.screen(
				screen_name=ImageLocation.RETRIEVE_DELIVER_DETAILS_SCREEN,
				image_to_compare="selected_deliver_pkg_btn",
				mouse_click=1,
				skip_sleep=True,
			)
			if result['success']:
				logger.info(f"{character.username} Delivered a package")
				return {"has_package": False}
			return self.process_package(character, is_retrieve=False)
		return {"has_package": False}

	def retrieve_package(self, character):
		pydirectinput.press("f8")
		is_active_mission = self.ocr.ocr_missions(
			search_area=SearchAreaLocation.ACTIVE_TAKEN_MISSIONS,
			search_text=self.active_mission_name,
			click=True,
		)

		if not is_active_mission.success:
			self.setup_mission()
		result = self.verify.screen(
			screen_name=ImageLocation.RETRIEVE_DELIVER_DETAILS_SCREEN,
			image_to_compare="selected_retrieve_pkg_btn",
			mouse_click=1,
			skip_sleep=True,
		)

		if result['success']:
			logger.info(f"{character.username} Retrieved a package")
			return {"has_package": True}
		return self.process_package(character, is_retrieve=True)

	def setup_mission(self):
		unselected_search_btn = self.verify.screen(
			screen_name=ImageLocation.ACTIVE_TAKEN_MISSIONS_SCREEN,
			image_to_compare="unselected_search_btn",
			mouse_click=1
		)
		reward_unsorted = self.verify.screen(
			screen_name=ImageLocation.SEARCH_FOR_MISSIONS_SCREEN,
			image_to_compare="reward_unsorted",
			mouse_click=1,
			mouse_clicks=2,
		)
		self.ocr.ocr_missions(
			search_area=SearchAreaLocation.AVAILABLE_MISSIONS,
			search_text=self.active_mission_name,
			scroll=True,
			click=True
		)
		take_mission_details_btn = self.verify.screen(
			screen_name=ImageLocation.MISSION_DETAILS_SCREEN,
			image_to_compare="take_mission_details_btn",
			mouse_click=1,
		)
		take_mission_confirm_btn = self.verify.screen(
			screen_name=ImageLocation.CONFIRMATION_SCREEN,
			image_to_compare="take_mission_confirm_btn",
			mouse_click=1,
		)


if __name__ == "__main__":
	retrieve_status = True
	all_active_characters = CharacterQuerySet.get_active_characters()
	obj = DUMissions()
	for character in all_active_characters:
		# character = CharacterQuerySet.read_character_by_username(character.username)

		character_username = character.username
		character_email = character.email
		character_password = character.password

		if retrieve_status:
			# sleep(3)
			retrieve_status = obj.retrieve_package(character)
			# self.du_characters.logout()
		else:
			deliver_status = obj.deliver_package(character)
			# self.package_count = max(self.package_count - 1, 0)
			# du_characters.logout()
		# continue

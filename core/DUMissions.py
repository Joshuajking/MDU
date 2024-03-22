import random
from time import sleep

import pydirectinput
import pyperclip

from config.config_manager import ConfigManager
from logs.logging_config import logger
from models.models import SearchAreaLocation, ImageLocation
from querysets.querysets import CharacterQuerySet, SearchAreaQuerySet
from utils.special_mission_ocr import OCREngine
from utils.verify_screen import VerifyScreen


class DUMissions:
	image_list = ["selected_deliver_pkg_btn", "selected_retrieve_pkg_btn"]
	search_text_list = ["RETRIEVE PACKAGE", "DELIVER PACKAGE"]

	def __init__(self):
		self.config_manager = ConfigManager()
		self.verify = VerifyScreen()
		self.ocr = OCREngine()
		self.active_mission_name = self.config_manager.get_value("config.active_mission_name")
		self.character = None

	def get_package_coords(self):
		orign = SearchAreaQuerySet.get_searcharea_by_name(name=SearchAreaLocation.ORIGIN_POS)

		origin_coords = self.verify.screen(
			screen_name=ImageLocation.MISSION_DETAILS_SCREEN,
			image_to_compare="copy_coords",
			confidence=0.8,
			mouse_click=True,
		)

		origin_pos = pyperclip.paste()
		print(origin_pos)

		dest_coords = self.verify.screen(
			screen_name=ImageLocation.MISSION_DETAILS_SCREEN,
			image_to_compare="copy_coords",
			confidence=0.8,
			mouse_click=True,
		)

		dest_pos = pyperclip.paste()

		# title = self.active_mission_name
		# mission = MissionQuerySet.update_mission(title, {
		# 	"origin_pos": origin_pos,
		# 	"destination_pos": dest_pos,
		# })

		return origin_pos, dest_pos

	def ocr_RETRIEVE_DELIVERY_STATUS(self):
		for text in self.search_text_list:
			mission_package_btn = self.ocr.ocr_missions(
				search_area=SearchAreaLocation.RETRIEVE_DELIVERY_STATUS,
				search_text=text,
			)
			if mission_package_btn["text"] == "RETRIEVE PACKAGE":
				logger.debug(f"{self.character.username}: mission to far to {mission_package_btn['text']}")
				return {"has_package": False}
			elif mission_package_btn["text"] == "DELIVER PACKAGE":
				logger.debug(f"{self.character.username}: mission to far to {mission_package_btn['text']}")
				return {"has_package": True}
			continue
		raise Exception(f"No package found for {text}")

	def is_active_mission(self):
		sleep(random.uniform(1, 2))
		is_active_mission = self.ocr.ocr_missions(
			search_area=SearchAreaLocation.ACTIVE_TAKEN_MISSIONS,
			search_text=self.active_mission_name,
			click=True,
		)
		return is_active_mission

	def get_package(self):
		for image_name in self.image_list:
			result = self.verify.screen(
				screen_name=ImageLocation.RETRIEVE_DELIVER_DETAILS_SCREEN,
				image_to_compare=image_name,
				mouse_click=True,
				mouse_clicks=2,
				skip_sleep=True,
			)
			if result.get('success'):
				if image_name == "selected_deliver_pkg_btn":
					logger.debug(f"Package delivered")
					return {"has_package": False}
				elif image_name == "selected_retrieve_pkg_btn":
					logger.debug(f"Package retrieved")
					return {"has_package": True}
		return self.ocr_RETRIEVE_DELIVERY_STATUS()

	def select_package(self):
		unselected_search_btn = self.verify.screen(
			screen_name=ImageLocation.ACTIVE_TAKEN_MISSIONS_SCREEN,
			image_to_compare="unselected_search_btn",
			mouse_click=True,
		)
		reward_unsorted = self.verify.screen(
			screen_name=ImageLocation.SEARCH_FOR_MISSIONS_SCREEN,
			image_to_compare="reward_unsorted",
			mouse_click=True,
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
			mouse_click=True,
		)
		take_mission_confirm_btn = self.verify.screen(
			screen_name=ImageLocation.CONFIRMATION_SCREEN,
			image_to_compare="take_mission_confirm_btn",
			mouse_click=True,
		)
		result = self.verify.screen(
			screen_name=ImageLocation.RETRIEVE_DELIVER_DETAILS_SCREEN,
			image_to_compare="selected_retrieve_pkg_btn",
			mouse_click=True,
			skip_sleep=True,
		)
		if result.get("success"):
			logger.debug(f"Package retrieved")
			return {"has_package": True}
		return self.ocr_RETRIEVE_DELIVERY_STATUS()

	def process_package(self, character):
		self.character = character
		logger.debug(f"Opening mission menu")
		pydirectinput.press("f8")

		is_active_mission = self.is_active_mission()
		logger.info(
			f"{self.character.username}: mission status {is_active_mission.get('success')}"
			if is_active_mission.get('success') else f"{self.character.username}: mission status"
		)
		if is_active_mission.get('success'):
			logger.debug(f"Processing active mission")
			return self.get_package()
		else:
			logger.debug(f"Aquiring mission")
			return self.select_package()


if __name__ == "__main__":
	retrieve_status = True
	all_active_characters = CharacterQuerySet.get_active_characters()
	obj = DUMissions()
	obj.process_package()

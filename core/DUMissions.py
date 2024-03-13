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
		self.verify = VerifyScreen()
		self.ocr = OCREngine()
		self.active_mission_name = self.config_manager.get_value("config.active_mission_name")

	def get_package_coords(self):
		orign = SearchAreaQuerySet.get_searcharea_by_name(name=SearchAreaLocation.ORIGIN_POS)

		origin_coords = self.verify.screen(
			screen_name=ImageLocation.MISSION_DETAILS_SCREEN,
			image_to_compare="copy_coords",
			confidence=0.8,
			# region=orign,
			mouse_click=True,
		)

		origin_pos = pyperclip.paste()
		print(origin_pos)

		dest_coords = self.verify.screen(
			screen_name=ImageLocation.MISSION_DETAILS_SCREEN,
			image_to_compare="copy_coords",
			confidence=0.8,
			region=(1457, 605, 1521, 654),
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
			continue
		logger.error(f"{search_text_list} could not be found")
		raise ValueError()

	def process_package(self, retries=2):
		pydirectinput.press("f8")

		is_active_mission = self.ocr.ocr_missions(
			search_area=SearchAreaLocation.ACTIVE_TAKEN_MISSIONS,
			search_text=self.active_mission_name,
			click=True,
		)

		if is_active_mission.success:
			image_list = ["selected_deliver_pkg_btn", "selected_retrieve_pkg_btn"]

			for image_to_compare in image_list:
				result = self.verify.screen(
					screen_name=ImageLocation.RETRIEVE_DELIVER_DETAILS_SCREEN,
					image_to_compare=image_to_compare,
					mouse_click=True,
					mouse_clicks=2,
					skip_sleep=True,
				)

				if result['success'] and image_to_compare == "selected_deliver_pkg_btn":
					action = "Delivered"
					return {"has_package": False}
				elif result['success'] and image_to_compare == "selected_retrieve_pkg_btn":
					action = "Retrieved"
					return {"has_package": True}
				else:
					return self.ocr_RETRIEVE_DELIVERY_STATUS()
		else:
			unselected_search_btn = self.verify.screen(
				screen_name=ImageLocation.ACTIVE_TAKEN_MISSIONS_SCREEN,
				image_to_compare="unselected_search_btn",
				mouse_click=True,
				mouse_clicks=2
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
				mouse_clicks=2
			)
			image_list = ["selected_deliver_pkg_btn", "selected_retrieve_pkg_btn"]

			for image_to_compare in image_list:
				result = self.verify.screen(
					screen_name=ImageLocation.RETRIEVE_DELIVER_DETAILS_SCREEN,
					image_to_compare=image_to_compare,
					mouse_click=True,
					mouse_clicks=2,
					skip_sleep=True,
				)

				if result['success'] and image_to_compare == "selected_deliver_pkg_btn":
					action = "Delivered"
					return {"has_package": False}
				elif result['success'] and image_to_compare == "selected_retrieve_pkg_btn":
					action = "Retrieved"
					return {"has_package": True}
				continue
			return self.ocr_RETRIEVE_DELIVERY_STATUS()


if __name__ == "__main__":
	retrieve_status = True
	all_active_characters = CharacterQuerySet.get_active_characters()
	obj = DUMissions()
	obj.process_package()

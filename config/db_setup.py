# import os.path
# import sqlite3
# import uuid
# from datetime import datetime
#
# import pyautogui
# from logs.logging_config import logger
# from sqlmodel import SQLModel, Session
#
# from models.models import SearchArea, Character, Image
# from path_router import DirectoryPaths
# from config.config_manager import ConfigManager
# from querysets.querysets import engine
# from utils.data_preprocessor import DataPreprocessor
#
#
# class DbConfig:
# 	def __init__(self, images_dir=None):
# 		self.config_manager = ConfigManager()
# 		self.images_dir = images_dir or os.path.relpath(DirectoryPaths.DU_IMAGES_DIR)
#
# 	def load_search_areas_to_db(self):
# 		# Define search areas
# 		search_areas = [
# 			SearchArea(region_name="active_missions", left=530, top=830, right=909,
# 			           bottom=1017),
#
# 			SearchArea(region_name="mission_package_area", left=1221, top=724,
# 			           right=1470, bottom=756),
#
# 			SearchArea(region_name="scrollable_area", left=890, top=275, right=1040,
# 			           bottom=505),
#
# 		]
#
# 		# Create tables
# 		SQLModel.metadata.create_all(engine)
#
# 		# Insert search areas into database
# 		with Session(engine) as session:
# 			for search_area in search_areas:
# 				session.add(search_area)
# 			session.commit()
#
# 	def manual_load_character(self):
# 		data = [
# 			("username", "password", "email"),
# 			("username", "password", "email"),
# 			("username", "password", "email"),
# 		]
#
# 		characters = []
# 		for username, password, email in data:
# 			character = Character(username=username, email=email, password=password)
# 			characters.append(character)
#
# 		with Session(engine) as session:
# 			for character in characters:
# 				session.add(character)
# 			session.commit()
#
# 	def load_characters_to_db(self):
# 		with Session(engine) as session:
# 			Character.__table__.create(engine, checkfirst=True)
# 			for character_name, character_data in var.items():
# 				email = character_data.get("email")
# 				pwd = character_data.get("pwd")
# 				character = Character(username=character_name, email=email, password=pwd)
# 				session.add(character)
# 			session.commit()
#
# 	def load_image_entries_to_db(self):
# 		count = 0
# 		with Session(engine) as session:
# 			for location in os.listdir(self.images_dir):
# 				location_dir = os.path.join(self.images_dir, location)
# 				if os.path.isdir(location_dir):
# 					for image_name in os.listdir(location_dir):
# 						image_path = os.path.join(location_dir, image_name)
# 						if os.path.isfile(image_path):
# 							# Check if the image already exists in the database
# 							existing_image = session.query(Image).filter_by(image_name=image_name,
# 							                                                image_location=location).first()
# 							if not existing_image:
# 								# Update the image URL to the new path
# 								image_url = image_path
# 								new_image = Image(image_name=image_name, image_location=location, image_url=image_url)
# 								session.add(new_image)
# 								new_image.created_at = datetime.now()
# 								count += 1
# 							else:
# 								# Update existing image URL if it has changed
# 								if existing_image.image_url != image_path:
# 									existing_image.image_url = image_path
# 									count += 1
# 			if count > 0:
# 				logger.info(f"Total images updated: {count}")
# 				session.commit()
# 			else:
# 				logger.info("No new images or existing images updated")
#
# 	@staticmethod
# 	def create_db_and_tables():
# 		SQLModel.metadata.create_all(engine)
#
# 	@staticmethod
# 	def delete_image_from_db():
# 		from querysets.querysets import ImageQuerySet
# 		ImageQuerySet.delete_image_by_id(id='0b1d2e01141d4590bfe3e5c5a560c849')
#
# 	@staticmethod
# 	def get_image_bbox(image_path, region_name, confidence=0.7):
# 		from querysets.querysets import SearchAreaQuerySet
# 		screen_coords = pyautogui.locateOnScreen(image_path, minSearchTime=3, confidence=confidence)
# 		# for screen_coords in pyautogui.locateAllOnScreen(r"C:\Repositories\Dual Universe\Missions Dual Universe\data\search_areas\ORBITAL_HUD_LANDED.png"):
# 		# 	screen_coords = screen_coords
# 		if screen_coords is not None:
# 			left, top, width, height = screen_coords
# 			right = left + width
# 			bottom = top + height
# 			center_x = left + width // 2
# 			center_y = top + height // 2
# 			pyautogui.moveTo(center_x, center_y)
# 			SearchAreaQuerySet.create_or_update_search_area(region_name, {
# 				"left": int(left),
# 				"top": int(top),
# 				"right": int(right),
# 				"bottom": int(bottom),
# 				"center_x": int(center_x),
# 				"center_y": int(center_y)
# 			})
# 			return
# 		raise ValueError(f"region_name: {region_name} was not found in")
#
#
#
# if __name__ == '__main__':
# 	obj = DbConfig()
# 	# obj.create_db_and_tables()
# 	obj.manual_load_character()
# # obj.load_image_entries_to_db()
#
# # obj.delete_image_from_db()
# #
# # from models.models import SearchAreaLocation
# #
# # area = {
# # 	"ACTIVE_TAKEN_MISSIONS": {
# # 		"region_name": SearchAreaLocation.ACTIVE_TAKEN_MISSIONS,
# # 		"image_path": r"C:\Repositories\Dual Universe\Missions Dual Universe\data\search_areas\ACTIVE_TAKEN_MISSIONS.png"
# # 	},
# # 	"AVAILABLE_MISSIONS": {
# # 		"region_name": SearchAreaLocation.AVAILABLE_MISSIONS,
# # 		"image_path": r"C:\Repositories\Dual Universe\Missions Dual Universe\data\search_areas\AVAILABLE_MISSIONS.png"
# # 	},
# # 	"RETRIEVE_DELIVERY_STATUS": {
# # 		"region_name": SearchAreaLocation.RETRIEVE_DELIVERY_STATUS,
# # 		"image_path": r"C:\Repositories\Dual Universe\Missions Dual Universe\data\search_areas\unselected_deliver_package.png"
# # 	},
# # }
# #
# # obj.get_image_bbox(region_name=SearchAreaLocation.ACTIVE_TAKEN_MISSIONS,
# #                    image_path=r"C:\Repositories\Dual Universe\MDU\data\search_areas\ACTIVE_TAKEN_MISSIONS.png")
# #
# # obj.get_image_bbox(region_name=SearchAreaLocation.AVAILABLE_MISSIONS,
# #                image_path=r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 091333.png")
#
# # obj.get_image_bbox(region_name=SearchAreaLocation.RETRIEVE_DELIVERY_STATUS,
# #                    image_path=r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 091451.png")
#
# # obj.get_image_bbox(region_name=SearchAreaLocation.ABANDON_MISSION,
# #                image_path=r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 091601.png")
#
# # obj.get_image_bbox(region_name=SearchAreaLocation.WARP_TARGET_DEST,
# #                image_path=r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 092011.png")
#
# # obj.get_image_bbox(region_name=SearchAreaLocation.ORBITAL_HUD_LANDED,
# #                    image_path=r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 092202.png",
# #                    confidence=0.6,
# #                    )
# #
# # obj.get_image_bbox(region_name=SearchAreaLocation.SPACE_FUEL,
# #                    image_path=r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 093227.png")
# #
# # obj.get_image_bbox(region_name=SearchAreaLocation.ATMO_FUEL,
# #                    image_path=r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 093227.png")
#
# # region_dict = {
#
# # "DEST_INFO": {
# # 	"region_name": SearchAreaLocation.DEST_INFO,
# # 	"image_path": r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 085354.png"
# # },
# # "SAFE_ZONE": {
# # 	"region_name": SearchAreaLocation.SAFE_ZONE,
# # 	"image_path": r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 085458.png"
# # },
# # "RIDE": {
# # 	"region_name": SearchAreaLocation.RIDE,
# # 	"image_path": r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 085513.png"
# # },
# # "DISTANCE": {
# # 	"region_name": SearchAreaLocation.DISTANCE,
# # 	"image_path": r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 085507.png"
# # },
# # "STATUS": {
# # 	"region_name": SearchAreaLocation.STATUS,
# # 	"image_path": r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 085616.png"
# # },
# # "ORIGIN_INFO": {
# # 	"region_name": SearchAreaLocation.ORIGIN_INFO,
# # 	"image_path": r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 085344.png"
# # },
# # "MASS": {
# # 	"region_name": SearchAreaLocation.MASS,
# # 	"image_path": r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 085436.png"
# # },
# # "VOLUME": {
# # 	"region_name": SearchAreaLocation.VOLUME,
# # 	"image_path": r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 085447.png"
# # },
# # "REWARD_INFO": {
# # 	"region_name": SearchAreaLocation.REWARD_INFO,
# # 	"image_path": r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 085154.png"
# # },
# # "TITLE_INFO": {
# # 	"region_name": SearchAreaLocation.TITLE_INFO,
# # 	"image_path": r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 085603.png"
# # },
# # "ORIGIN_POS": {
# # 	"region_name": SearchAreaLocation.ORIGIN_POS,
# # 	"image_path": r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-03 014408.png"
# # },
# # "DEST_POS": {
# # 	"region_name": SearchAreaLocation.DEST_POS,
# # 	"image_path": r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-03 020140.png"
# # },
# # 	"ORBITAL_HUD_LANDED": {
# # 		"region_name": SearchAreaLocation.ORBITAL_HUD_LANDED,
# # 		"image_path": r"C:\Repositories\Dual Universe\Missions Dual Universe\data\search_areas\ORBITAL_HUD_LANDED.png"
# # 	},
# # }
# #
# # for key, value in region_dict.items():
# # 	region_name = value["region_name"]
# # 	image_path = value["image_path"]
# #
# # 	obj.get_image_bbox(region_name=region_name,
# # 	                   image_path=image_path)

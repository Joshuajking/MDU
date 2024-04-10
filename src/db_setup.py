import json
import os
import os.path
import uuid
from datetime import datetime

import pyautogui
from sqlmodel import SQLModel, Session, select

from router import DirectoryPaths
from settings import engine
from src.config_manager import ConfigManager
from src.logging_config import logger
from src.models import SearchArea, Image, Mission


class DbConfig:
	config_manager = ConfigManager()
	engine = engine

	def __init__(self, images_dir=None):
		self.config_manager = ConfigManager()
		self.images_dir = images_dir or os.path.relpath(DirectoryPaths.IMAGES_DIR)

	def create_db_and_tables(self):
		SQLModel.metadata.create_all(self.engine)

	def load_SearchArea_table(self):
		try:
			# Load the JSON data from the file
			file_path = os.path.join(DirectoryPaths.DATA_DIR, 'SearchArea_table.json')
			with open(file_path, "r") as json_file:
				json_data = json.load(json_file)

			with Session(self.engine) as session:
				for item in json_data:
					# item_dict = item.dict()
					existing_search_area = session.exec(select(SearchArea).filter_by(**item)).first()
					if existing_search_area:
						# logger.info(f"SearchArea already exists: {existing_search_area}")
						pass
					else:
						# Create a new Image instance with the data from the JSON
						search_area = SearchArea(**item)
						search_area.id = str(uuid.uuid4())
						# image.updated_at = datetime.now()
						search_area.created_at = datetime.now()
						search_area.updated_at = datetime.now()
						# Insert the Image instance into the table
						session.add(search_area)

				# Commit the transaction
				session.commit()
		except Exception as e:
			logger.error(f"Error loading table SearchArea_table.json: {e}")

	def load_Image_table(self):
		try:
			# Load the JSON data from the file
			file_path = os.path.join(DirectoryPaths.DATA_DIR, 'Image_table.json')
			with open(file_path, "r") as json_file:
				json_data = json.load(json_file)

			with Session(self.engine) as session:
				for item in json_data:
					# Check if an Image instance with the same data already exists
					existing_image = session.exec(select(Image).filter_by(**item)).first()
					if existing_image:
						# logger.info(f"Image already exists: {existing_image}")
						pass
					else:
						# Create a new Image instance with the data from the JSON
						image = Image(**item)
						image.id = str(uuid.uuid4())
						image.created_at = datetime.now()
						image.updated_at = datetime.now()
						# Insert the Image instance into the table
						session.add(image)

				# Commit the transaction
				session.commit()
		except Exception as e:
			logger.error(f"Error loading table Image_table.json: {e}")

	def load_Mission_table(self):
		try:
			# Load the JSON data from the file
			file_path = os.path.join(DirectoryPaths.DATA_DIR, 'Mission_table.json')
			with open(file_path, "r") as json_file:
				json_data = json.load(json_file)

			with Session(self.engine) as session:
				for item in json_data:
					# Check if an Image instance with the same data already exists
					existing_mission = session.exec(select(Mission).filter_by(**item)).first()
					if existing_mission:
						logger.info(f"Image already exists: {existing_mission}")
					else:
						# Create a new Image instance with the data from the JSON
						mission = Mission(**item)
						mission.id = str(uuid.uuid4())
						mission.created_at = datetime.now()
						mission.updated_at = datetime.now()
						# Insert the Image instance into the table
						session.add(mission)

				# Commit the transaction
				session.commit()
		except Exception as e:
			logger.error(f"Error loading table Mission_table.json: {e}")

	def load_image_entries_to_db(self):  # TODO: alters file path (main.py - data\du_images...) & (character_link.py - ..\data\du_images...) and keeps creating files in db
		count = 0
		with Session(self.engine) as session:
			for location in os.listdir(self.images_dir):
				location_dir = os.path.join(self.images_dir, location)
				if os.path.isdir(location_dir):
					for image_name in os.listdir(location_dir):
						image_path = os.path.join(location_dir, image_name)
						if os.path.isfile(image_path):
							# Check if the image already exists in the database
							existing_image = session.query(Image).filter_by(image_name=image_name,
							                                                image_location=location).first()
							if not existing_image:
								# Update the image URL to the new path
								image_url = image_path
								new_image = Image(image_name=image_name, image_location=location, image_url=image_url)
								session.add(new_image)
								new_image.created_at = datetime.now()
								count += 1
							else:
								# Update existing image URL if it has changed
								if existing_image.image_url != image_path:
									existing_image.image_url = image_path
									count += 1
			if count > 0:
				logger.info(f"Total images updated: {count}")
				session.commit()
			else:
				logger.info("No new images or existing images updated")

	def alt_load_image_entries_to_db(self):
		count = 0
		with Session(self.engine) as session:
			for location in os.listdir(self.images_dir):
				location_dir = os.path.join(self.images_dir, location)
				if os.path.isdir(location_dir):
					for image_name in os.listdir(location_dir):
						image_path = os.path.join(location_dir, image_name)
						if os.path.isfile(image_path):
							# Check if the image already exists in the database
							existing_image = session.query(Image).filter_by(image_name=image_name,
							                                                image_location=location).first()
							if not existing_image:
								# Update the image URL to the new path
								image_url = os.path.join('data', 'images', location, image_name)
								new_image = Image(image_name=image_name, image_location=location, image_url=image_url)
								session.add(new_image)
								new_image.created_at = datetime.now()
								count += 1
							else:
								# Update existing image URL if it has changed
								if existing_image.image_url != image_path:
									existing_image.image_url = os.path.join('data', 'images', location, image_name)
									count += 1
			if count > 0:
				logger.info(f"Total images updated: {count}")
				session.commit()
			else:
				logger.info("No new images or existing images updated")

	@staticmethod
	def get_image_bbox(image_path, region_name, confidence=0.7):
		from src.querysets import SearchAreaQuerySet
		screen_coords = pyautogui.locateOnScreen(image_path, minSearchTime=3, confidence=confidence)
		# for screen_coords in pyautogui.locateAllOnScreen(r"C:\Repositories\Dual Universe\Missions Dual Universe\data\bbox_images\ORBITAL_HUD_LANDED.png"):
		# 	screen_coords = screen_coords
		if screen_coords is not None:
			left, top, width, height = screen_coords
			right = left + width
			bottom = top + height
			center_x = left + width // 2
			center_y = top + height // 2
			pyautogui.moveTo(center_x, center_y)
			SearchAreaQuerySet.create_or_update_search_area(region_name, {
				"left": int(left),
				"top": int(top),
				"right": int(right),
				"bottom": int(bottom),
				"center_x": int(center_x),
				"center_y": int(center_y)
			})
			return
		raise ValueError(f"region_name: {region_name} was not found in")


if __name__ == '__main__':
	obj = DbConfig()
	# # obj.load_image_entries_to_db()
	obj.alt_load_image_entries_to_db()
	# # obj.create_db_and_tables()
	# # obj.load_Mission_table()
	# obj.load_Image_table()
	# obj.load_SearchArea_table()
	# obj.load_image_entries_to_db()

	# obj.delete_image_from_db()
	#
	# from model.model import SearchAreaLocation
	#
	# area = {
	# 	"ACTIVE_TAKEN_MISSIONS": {
	# 		"region_name": SearchAreaLocation.ACTIVE_TAKEN_MISSIONS,
	# 		"image_path": r"C:\Repositories\Dual Universe\Missions Dual Universe\data\bbox_images\ACTIVE_TAKEN_MISSIONS.png"
	# 	},
	# 	"AVAILABLE_MISSIONS": {
	# 		"region_name": SearchAreaLocation.AVAILABLE_MISSIONS,
	# 		"image_path": r"C:\Repositories\Dual Universe\Missions Dual Universe\data\bbox_images\AVAILABLE_MISSIONS.png"
	# 	},
	# 	"RETRIEVE_DELIVERY_STATUS": {
	# 		"region_name": SearchAreaLocation.RETRIEVE_DELIVERY_STATUS,
	# 		"image_path": r"C:\Repositories\Dual Universe\Missions Dual Universe\data\bbox_images\unselected_deliver_package.png"
	# 	},
	# }
	#
	# obj.get_image_bbox(region_name=SearchAreaLocation.ACTIVE_TAKEN_MISSIONS,
	#                    image_path=r"C:\Repositories\Dual Universe\MDU\data\bbox_images\ACTIVE_TAKEN_MISSIONS.png")
	#
	# obj.get_image_bbox(region_name=SearchAreaLocation.AVAILABLE_MISSIONS,
	#                image_path=r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 091333.png")

	# obj.get_image_bbox(region_name=SearchAreaLocation.RETRIEVE_DELIVERY_STATUS,
	#                    image_path=r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 091451.png")

	# obj.get_image_bbox(region_name=SearchAreaLocation.ABANDON_MISSION,
	#                image_path=r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 091601.png")

	# obj.get_image_bbox(region_name=SearchAreaLocation.WARP_TARGET_DEST,
	#                image_path=r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 092011.png")

	# obj.get_image_bbox(region_name=SearchAreaLocation.ORBITAL_HUD_LANDED,
	#                    image_path=r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 092202.png",
	#                    confidence=0.6,
	#                    )
	#
	# obj.get_image_bbox(region_name=SearchAreaLocation.SPACE_FUEL,
	#                    image_path=r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 093227.png")
	#
	# obj.get_image_bbox(region_name=SearchAreaLocation.ATMO_FUEL,
	#                    image_path=r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 093227.png")

	# region_dict = {

		# "DEST_INFO": {
		# 	"region_name": SearchAreaLocation.DEST_INFO,
		# 	"image_path": r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 085354.png"
		# },
		# "SAFE_ZONE": {
		# 	"region_name": SearchAreaLocation.SAFE_ZONE,
		# 	"image_path": r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 085458.png"
		# },
		# "RIDE": {
		# 	"region_name": SearchAreaLocation.RIDE,
		# 	"image_path": r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 085513.png"
		# },
		# "DISTANCE": {
		# 	"region_name": SearchAreaLocation.DISTANCE,
		# 	"image_path": r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 085507.png"
		# },
		# "STATUS": {
		# 	"region_name": SearchAreaLocation.STATUS,
		# 	"image_path": r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 085616.png"
		# },
		# "ORIGIN_INFO": {
		# 	"region_name": SearchAreaLocation.ORIGIN_INFO,
		# 	"image_path": r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 085344.png"
		# },
		# "MASS": {
		# 	"region_name": SearchAreaLocation.MASS,
		# 	"image_path": r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 085436.png"
		# },
		# "VOLUME": {
		# 	"region_name": SearchAreaLocation.VOLUME,
		# 	"image_path": r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 085447.png"
		# },
		# "REWARD_INFO": {
		# 	"region_name": SearchAreaLocation.REWARD_INFO,
		# 	"image_path": r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 085154.png"
		# },
		# "TITLE_INFO": {
		# 	"region_name": SearchAreaLocation.TITLE_INFO,
		# 	"image_path": r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-02 085603.png"
		# },
		# "ORIGIN_POS": {
		# 	"region_name": SearchAreaLocation.ORIGIN_POS,
		# 	"image_path": r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-03 014408.png"
		# },
		# "DEST_POS": {
		# 	"region_name": SearchAreaLocation.DEST_POS,
		# 	"image_path": r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-03 020140.png"
		# },
		# 	"ORBITAL_HUD_LANDED": {
		# 		"region_name": SearchAreaLocation.ORBITAL_HUD_LANDED,
		# 		"image_path": r"C:\Repositories\Dual Universe\Missions Dual Universe\data\bbox_images\ORBITAL_HUD_LANDED.png"
		# 	},
		# }
		# 	"GAME_CONSOLE_WINDOW": {
		# 		"region_name": SearchAreaLocation.GAME_CONSOLE_WINDOW,
		# 		"image_path": r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-03-28 180709.png"
		# 	},
		# }
		# 	"ATMO_FUEL": {
		# 		"region_name": SearchAreaLocation.ATMO_FUEL,
		# 		"image_path": r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-04-02 000644.png"
		# 	},
		# }
		# 	"WALLET_CURRENCY": {
		# 		"region_name": SearchAreaLocation.WALLET_CURRENCY,
		# 		"image_path": r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-04-01 200353.png"
		# 	},
		# }
		# 	"WALLET_RECIPIENT_LIST": {
		# 		"region_name": SearchAreaLocation.WALLET_RECIPIENT_LIST,
		# 		"image_path": r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-04-01 162042.png"
		# 	},
		# }
		# 	"RECIPIENT_SEARCH_AREA": {
		# 		"region_name": SearchAreaLocation.RECIPIENT_SEARCH_AREA,
		# 		"image_path": r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-04-01 162512.png"
		# 	},
	# }

	# for key, value in region_dict.items():
	# 	region_name = value["region_name"]
	# 	image_path = value["image_path"]
	#
	# 	obj.get_image_bbox(region_name=region_name,
	# 	                   image_path=image_path)

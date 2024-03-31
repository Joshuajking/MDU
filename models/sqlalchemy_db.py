import json
import os
import uuid
from datetime import datetime

from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session, select

from config.config_manager import ConfigManager
from logs.logging_config import logger
from models.models import SearchArea, Image, Mission
from path_router import DirectoryPaths
from querysets.querysets import engine


class DbConfig:
	config_manager = ConfigManager()
	# engine = create_engine(f"sqlite:///../database/test_db.db")
	engine = engine

	# engine = create_engine(
	# 	f"sqlite:///{os.path.join(DirectoryPaths.ROOT_DIR, config_manager.get_value('config.database'))}",
	# 	echo=False,
	# )

	def __init__(self, images_dir=None):
		self.config_manager = ConfigManager()
		self.images_dir = images_dir or os.path.relpath(DirectoryPaths.DU_IMAGES_DIR)
		self.__dump_table_SearchArea()
		self.__dump_table_Image()
		self.__dump_table_Mission()
		self.__create_db_and_tables()
		self.__load_Image_table()
		self.__load_SearchArea_table()
		self.__load_Mission_table()

	def __dump_table_Mission(self):
		try:
			with Session(self.engine) as session:
				query = session.exec(select(Mission)).all()
				excluded_fields = {'updated_at', 'created_at'}

			# Extract only the required fields for SearchArea
			filtered_data = []
			for data in query:
				filtered_data.append(
					{
						field_name: getattr(data, field_name)
						for field_name in data.model_dump().keys()
						if field_name not in excluded_fields
					}
				)

			# Dump the data to a JSON file
			file_path = os.path.join(DirectoryPaths.DB_DUMP_DIR, 'Mission_table.json')
			with open(file_path, "w+") as json_file:
				json.dump(filtered_data, json_file, indent=4)
		except Exception as e:
			logger.error(f"Error dumping table Mission_table: {e}")

	def __dump_table_Image(self):
		try:
			with Session(self.engine) as session:
				query = session.exec(select(Image)).all()
				excluded_fields = {'updated_at', 'created_at'}

			# Extract only the required fields for SearchArea
			filtered_data = []
			for data in query:
				filtered_data.append(
					{
						field_name: getattr(data, field_name)
						for field_name in data.model_dump().keys()
						if field_name not in excluded_fields
					}
				)

			# Dump the data to a JSON file
			file_path = os.path.join(DirectoryPaths.DB_DUMP_DIR, 'Image_table.json')
			with open(file_path, "w+") as json_file:
				json.dump(filtered_data, json_file, indent=4)
		except Exception as e:
			logger.error(f"Error dumping table Image_table: {e}")

	def __dump_table_SearchArea(self):
		try:
			with Session(self.engine) as session:
				query = session.exec(select(SearchArea)).all()
				excluded_fields = {'updated_at', 'created_at'}

			# Extract only the required fields for SearchArea
			filtered_data = []
			for data in query:
				filtered_data.append(
					{
						field_name: getattr(data, field_name)
						for field_name in data.model_dump().keys()
						if field_name not in excluded_fields
					}
				)

			# Dump the data to a JSON file
			file_path = os.path.join(DirectoryPaths.DB_DUMP_DIR, 'SearchArea_table.json')
			with open(file_path, "w+") as json_file:
				json.dump(filtered_data, json_file, indent=4)
		except Exception as e:
			logger.error(f"Error dumping table SearchArea_table: {e}")

	def __create_db_and_tables(self):
		SQLModel.metadata.create_all(self.engine)

	def __load_SearchArea_table(self):
		try:
			# Load the JSON data from the file
			file_path = os.path.join(DirectoryPaths.DB_DUMP_DIR, 'SearchArea_table.json')
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

	def __load_Image_table(self):
		try:
			# Load the JSON data from the file
			file_path = os.path.join(DirectoryPaths.DB_DUMP_DIR, 'Image_table.json')
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

	def __load_Mission_table(self):
		try:
			# Load the JSON data from the file
			file_path = os.path.join(DirectoryPaths.DB_DUMP_DIR, 'Mission_table.json')
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

	def load_image_entries_to_db(self):
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


if __name__ == "__main__":
	config = DbConfig()
	config.dump_table_SearchArea()
	config.dump_table_Image()
	config.dump_table_Mission()
	config.create_db_and_tables()
	config.load_Image_table()
	config.load_SearchArea_table()
	config.load_Mission_table()

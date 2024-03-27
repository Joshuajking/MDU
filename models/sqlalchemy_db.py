import json
import os
import uuid
from datetime import datetime

import sqlalchemy
from sqlalchemy.orm import load_only

from logs.logging_config import logger
from sqlalchemy import create_engine, text, insert
from sqlmodel import SQLModel, Session, select

from config.config_manager import ConfigManager
from models import SearchArea, ImageLocation, Image, Mission
from path_router import DirectoryPaths


class DbConfig:
	config_manager = ConfigManager()
	memory_engine = create_engine(f"sqlite:///:memory:")

	engine = create_engine(
		f"sqlite:///{os.path.join(DirectoryPaths.ROOT_DIR, config_manager.get_value('config.database'))}",
		echo=False,
	)

	def __init__(self, images_dir=None):
		self.config_manager = ConfigManager()
		self.images_dir = images_dir or os.path.relpath(DirectoryPaths.DU_IMAGES_DIR)

	def dump_table_Mission(self):
		try:
			with Session(self.engine) as session:
				query = session.exec(select(Mission)).all()
				excluded_fields = {'updated_at', 'created_at', 'id'}

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
			file_path = "../config/db_table/Mission_table.json"
			with open(file_path, "w+") as json_file:
				json.dump(filtered_data, json_file, indent=4)
		except Exception as e:
			logger.error(f"Error dumping table Mission_table: {e}")

	def dump_table_Image(self):
		try:
			with Session(self.engine) as session:
				query = session.exec(select(Image)).all()
				excluded_fields = {'updated_at', 'created_at', 'id'}

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
			file_path = "../config/db_table/Image_table.json"
			with open(file_path, "w+") as json_file:
				json.dump(filtered_data, json_file, indent=4)
		except Exception as e:
			logger.error(f"Error dumping table Image_table: {e}")

	def dump_table_SearchArea(self):
		try:
			with Session(self.engine) as session:
				query = session.exec(select(SearchArea)).all()
				excluded_fields = {'updated_at', 'created_at', 'id'}

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
			file_path = "../config/db_table/SearchArea_table.json"
			with open(file_path, "w+") as json_file:
				json.dump(filtered_data, json_file, indent=4)
		except Exception as e:
			logger.error(f"Error dumping table SearchArea_table: {e}")

	def create_db_and_tables(self):
		SQLModel.metadata.create_all(self.engine)

	def load_SearchArea_table(self):
		with Session(self.engine) as session:
			pass

	def load_Image_table(self):
		try:
			# Load the JSON data from the file
			file_path = "../config/db_table/Image_table.json"
			with open(file_path, "r") as json_file:
				json_data = json.load(json_file)

			with Session(self.memory_engine) as session:
				for item in json_data:
					# item_dict = item.dict()
					# Create a new Image instance with the data from the JSON
					image = Image(**item)
					image.id = uuid.uuid4()
					# image.updated_at = datetime.now()
					image.created_at = datetime.now()
					# Insert the Image instance into the table
					session.add(image)

				# Commit the transaction
				session.commit()
		except Exception as e:
			logger.error(f"Error loading table Image_table.json: {e}")

	def load_Mission_table(self):
		with Session(self.engine) as session:
			pass


if __name__ == "__main__":
	config = DbConfig()
	config.dump_table_SearchArea()
	config.dump_table_Image()
	config.dump_table_Mission()
# config.load_Image_table()

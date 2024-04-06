import json
import os
from collections import OrderedDict

from sqlmodel import Session, select

from config_manager import ConfigManager
from logging_config import logger
from models import SearchArea, Image, Mission
from querysets import engine
from router import DirectoryPaths


class DumpDataBase:
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
		self.__dump_table_Mission()
		self.__dump_table_SearchArea()
		self.__dump_table_Image()

	def __dump_table_Mission(self):
		try:
			with Session(self.engine) as session:
				query = session.exec(select(Mission)).all()
				excluded_fields = {'updated_at', 'created_at'}
			# Extract only the required fields for SearchArea
			filtered_data = []
			for data in query:
				ordered_data = OrderedDict()
				for field_name in data.model_dump().keys():
					if field_name not in excluded_fields:
						ordered_data[field_name] = getattr(data, field_name)
				filtered_data.append(ordered_data)

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
				ordered_data = OrderedDict()
				for field_name in data.model_dump().keys():
					if field_name not in excluded_fields:
						ordered_data[field_name] = getattr(data, field_name)
				filtered_data.append(ordered_data)

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
				ordered_data = OrderedDict()
				for field_name in data.model_dump().keys():
					if field_name not in excluded_fields:
						ordered_data[field_name] = getattr(data, field_name)
				filtered_data.append(ordered_data)

			# Dump the data to a JSON file
			file_path = os.path.join(DirectoryPaths.DB_DUMP_DIR, 'SearchArea_table.json')
			with open(file_path, "w+") as json_file:
				json.dump(filtered_data, json_file, indent=4)
		except Exception as e:
			logger.error(f"Error dumping table SearchArea_table: {e}")


if __name__ == '__main__':
	obj = DumpDataBase()

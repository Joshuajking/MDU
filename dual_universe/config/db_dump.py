import json
import os
from collections import OrderedDict

from loguru import logger
from sqlmodel import Session, select

from dual_universe.config.config_manager import ConfigMixin
from dual_universe.settings import ASSETS_DIR, engine
from dual_universe.src.models.image_model import Image
from dual_universe.src.models.mission_model import Mission
from dual_universe.src.models.search_area_model import SearchArea


class DumpDataBase(ConfigMixin):
    def __init__(self):
        super().__init__()
        self.engine = engine
        self.__dump_table_Mission()
        self.__dump_table_SearchArea()
        self.__dump_table_Image()

    def __dump_table_Mission(self):
        try:
            with Session(self.engine) as session:
                query = session.exec(select(Mission)).all()
                excluded_fields = {"updated_at", "created_at"}
            # Extract only the required fields for SearchArea
            filtered_data = []
            for data in query:
                ordered_data = OrderedDict()
                for field_name in data.model_dump().keys():
                    if field_name not in excluded_fields:
                        ordered_data[field_name] = getattr(data, field_name)
                filtered_data.append(ordered_data)

            # Dump the data to a JSON file
            file_path = os.path.join(ASSETS_DIR, "mission_table.json")
            with open(file_path, "w+") as json_file:
                json.dump(filtered_data, json_file, indent=4)
        except Exception as e:
            logger.error(f"Error dumping table Mission_table: {e}")

    def __dump_table_Image(self):
        try:
            with Session(self.engine) as session:
                query = session.exec(select(Image)).all()
                excluded_fields = {"updated_at", "created_at"}
            # Extract only the required fields for SearchArea
            filtered_data = []
            for data in query:
                ordered_data = OrderedDict()
                for field_name in data.model_dump().keys():
                    if field_name not in excluded_fields:
                        ordered_data[field_name] = getattr(data, field_name)
                filtered_data.append(ordered_data)

            # Dump the data to a JSON file
            file_path = os.path.join(ASSETS_DIR, "image_table.json")
            with open(file_path, "w+") as json_file:
                json.dump(filtered_data, json_file, indent=4)
        except Exception as e:
            logger.error(f"Error dumping table Image_table: {e}")

    def __dump_table_SearchArea(self):
        try:
            with Session(self.engine) as session:
                query = session.exec(select(SearchArea)).all()
                excluded_fields = {"updated_at", "created_at"}
            # Extract only the required fields for SearchArea
            filtered_data = []
            for data in query:
                ordered_data = OrderedDict()
                for field_name in data.model_dump().keys():
                    if field_name not in excluded_fields:
                        ordered_data[field_name] = getattr(data, field_name)
                filtered_data.append(ordered_data)

            # Dump the data to a JSON file
            file_path = os.path.join(ASSETS_DIR, "searcharea_table.json")
            with open(file_path, "w+") as json_file:
                json.dump(filtered_data, json_file, indent=4)
        except Exception as e:
            logger.error(f"Error dumping table SearchArea_table: {e}")


if __name__ == "__main__":
    obj = DumpDataBase()

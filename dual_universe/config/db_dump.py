import json
import os
from collections import OrderedDict

from sqlmodel import Session, select, SQLModel

from dual_universe.config.config_manager import ConfigMixin
from dual_universe.logs.logging_config import logger
from dual_universe.settings import CONFIG_DIR, db_engine
from dual_universe.src.models.image_model import Image
from dual_universe.src.models.mission_model import Mission
from dual_universe.src.models.search_area_model import SearchArea


class DumpDataBase(ConfigMixin):
    def __init__(self):
        super().__init__()
        self.engine = db_engine
        self.model_method_mapping = {
            "image": self.dump_table_Image,
            "mission": self.dump_table_Mission,
            "searcharea": self.dump_table_SearchArea,
        }

    def dump_table_Mission(self):
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
            file_path = os.path.join(CONFIG_DIR, "mission_table.json")
            with open(file_path, "w+") as json_file:
                json.dump(filtered_data, json_file, indent=4)
        except Exception as e:
            logger.error(f"Error dumping table Mission_table: {e}")

    def dump_table_Image(self):
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
            file_path = os.path.join(CONFIG_DIR, "image_table.json")
            with open(file_path, "w+") as json_file:
                json.dump(filtered_data, json_file, indent=4)
        except Exception as e:
            logger.error(f"Error dumping table Image_table: {e}")

    def dump_table_SearchArea(self):
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
            file_path = os.path.join(CONFIG_DIR, "searcharea_table.json")
            with open(file_path, "w+") as json_file:
                json.dump(filtered_data, json_file, indent=4)
        except Exception as e:
            logger.error(f"Error dumping table SearchArea_table: {e}")

    def process_model(self, model_class: SQLModel):
        # Look up the method from the mapping using the model class
        method = self.model_method_mapping.get(model_class)

        if method:
            # Call the method without any arguments
            method()
        else:
            raise ValueError(f"No method found for model '{model_class.__name__}'")


if __name__ == "__main__":
    obj = DumpDataBase()
    obj.dump_table_SearchArea()

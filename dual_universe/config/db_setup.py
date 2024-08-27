import json
import os
import os.path
import uuid
from datetime import datetime

import pyautogui
from loguru import logger
from sqlmodel import SQLModel, Session, select

from dual_universe.config.config_manager import ConfigMixin
from dual_universe.settings import ASSETS_DIR
from dual_universe.settings import engine
from dual_universe.src.models.character_model import Character
from dual_universe.src.models.image_model import Image
from dual_universe.src.models.mission_model import Mission, MissionMetadata
from dual_universe.src.models.search_area_model import SearchArea
from dual_universe.src.querysets.search_area_queryset import SearchAreaQuerySet
from dual_universe.src.utils.find_existing_item import find_existing_item


class DbChecker:
    def __init__(self, db_engine, table_data):
        self.db_engine = db_engine
        self.table_data = table_data
        # self.table_name = table_name
        self.errors = []

    def is_table_valid(self):
        """check if table exists"""
        # Implement your first check logic here
        try:
            with Session(self.db_engine) as session:
                _table_name = select(self.table_data)
                results = session.exec(_table_name).first()
        except Exception as exc:
            logger.error(f"Error loading table: {exc}")
        if isinstance(results, self.table_data):
            logger.success(f"{_table_name} - OK")
        self.errors.append(f"{_table_name} - Does Not Exist")

    def is_file_valid(self):
        # Implement your second check logic here
        table_name = self.table_data.__tablename__
        # Load the JSON data from the file
        file_path = os.path.join(ASSETS_DIR, f"{table_name}_table.json")

        if not os.path.exists(file_path):
            with open(file_path, "w") as file:
                pass
            return False
        if os.path.getsize(file_path) > 0:
            try:
                with open(file_path, "r") as json_file:
                    json_data = json.load(json_file)
                    return True  # File is valid and contains JSON data
            except json.JSONDecodeError:
                return False  # JSON is invalid
        else:
            return False  # File is empty

    def is_data_valid(self):
        # Implement your third check logic here
        table_name = self.table_data.__tablename__
        # Load the JSON data from the file
        file_path = os.path.join(ASSETS_DIR, f"{table_name}_table.json")

        try:
            with open(file_path, "r") as json_file:
                json_data = json.load(json_file)

            with Session(self.db_engine) as session:
                for item in json_data:
                    existing_item, model_class = find_existing_item(
                        session, self.table_data, **item
                    )
                    if existing_item:
                        logger.info(
                            f"{model_class.__name__} already exists: {existing_item}"
                        )
                    else:
                        # Create a new instance of the model class with the data from the JSON
                        new_record = model_class(**item)
                        new_record.id = str(uuid.uuid4())
                        new_record.created_at = datetime.now()
                        new_record.updated_at = datetime.now()
                        session.add(new_record)
                        logger.info(
                            f"Inserted new record into {table_name}: {new_record}"
                        )

                session.commit()
                logger.debug(f"{table_name} table loaded")
            return True
        except Exception as exc:
            logger.error(f"Error processing data for {table_name}: {exc}")
            self.errors.append(f"Error processing data for {table_name}: {exc}")
            return False

    def is_valid(self):
        self.errors.clear()

        # Call each check method sequentially
        if self.is_table_valid():
            return True
        if not self.is_file_valid():
            return False
        if self.is_data_valid():
            return True

        return False


class DbConfig(ConfigMixin, DbChecker):
    def __init__(self, db_engine=engine):
        super().__init__()
        self.db_engine = db_engine
        self.images_dir = os.path.join(ASSETS_DIR)
        self.create_db_and_tables()

    def create_db_and_tables(self):
        try:
            SQLModel.metadata.create_all(self.db_engine)
        except Exception as exc:
            logger.error(exc)
            raise exc

    def load_SearchArea_table(self):
        try:
            # Load the JSON data from the file
            file_path = os.path.join(ASSETS_DIR, "SearchArea_table.json")
            with open(file_path, "r") as json_file:
                json_data = json.load(json_file)

            with Session(self.db_engine) as session:
                for item in json_data:
                    # item_dict = item.dict()
                    existing_search_area = session.exec(
                        select(SearchArea).filter_by(**item)
                    ).first()
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
            file_path = os.path.join(ASSETS_DIR, "image_table.json")
            with open(file_path, "r") as json_file:
                json_data = json.load(json_file)

            with Session(self.db_engine) as session:
                for item in json_data:
                    # Check if an Image instance with the same data already exists
                    existing_image = session.exec(
                        select(Image).filter_by(**item)
                    ).first()
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
                logger.success(f"Image table loaded")
                session.commit()
        except Exception as e:
            logger.error(f"Error loading table Image_table.json: {e}")

    def load_Mission_table(self):
        try:
            with Session(self.db_engine) as session:
                _Mission = select(Mission)
                results = session.exec(_Mission).first()
                if isinstance(results, Mission):
                    logger.success("Mission_table - OK")
                else:
                    self.load_Mission_table()
            # Load the JSON data from the file
            file_path = os.path.join(ASSETS_DIR, "Mission_table.json")
            with open(file_path, "r") as json_file:
                json_data = json.load(json_file)

            with Session(self.db_engine) as session:
                for item in json_data:
                    # Check if an Image instance with the same data already exists
                    existing_mission = session.exec(
                        select(Mission).filter_by(**item)
                    ).first()
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
                logger.debug(f"Mission table loaded")
                session.commit()
        except Exception as e:
            logger.error(f"Error loading table Mission_table.json: {e}")

    def load_image_entries_to_db(self):
        count = 0
        with Session(self.db_engine) as session:
            for location in os.listdir(self.images_dir):
                location_dir = os.path.join(self.images_dir, location)
                if os.path.isdir(location_dir):
                    for image_name in os.listdir(location_dir):
                        image_path = os.path.join(location_dir, image_name)
                        if os.path.isfile(image_path):
                            try:
                                # Attempt to open the file to ensure it's accessible
                                with open(image_path, "rb") as f:
                                    f.read(
                                        1
                                    )  # Read the first byte to ensure the file is not corrupted or inaccessible

                                # Check if the image already exists in the database
                                existing_image = (
                                    session.query(Image)
                                    .filter_by(
                                        image_name=image_name, image_location=location
                                    )
                                    .first()
                                )
                                if not existing_image:
                                    # Update the image URL to the new path
                                    image_url = image_path
                                    new_image = Image(
                                        image_name=image_name,
                                        image_location=location,
                                        image_url=image_url,
                                    )
                                    session.add(new_image)
                                    new_image.created_at = datetime.now()
                                    count += 1
                                else:
                                    # Update existing image URL if it has changed
                                    if existing_image.image_url != image_path:
                                        existing_image.image_url = image_path
                                        count += 1
                            except Exception as e:
                                # Log an error if the file can't be opened
                                logger.error(f"Could not open file {image_path}: {e}")
            if count > 0:
                logger.info(f"Total images updated: {count}")
                session.commit()
            else:
                logger.info("No new images or existing images updated")

    def alt_load_image_entries_to_db(self):
        count = 0
        with Session(self.db_engine) as session:
            for location in os.listdir(self.images_dir):
                location_dir = os.path.join(self.images_dir, location)
                if os.path.isdir(location_dir):
                    for image_name in os.listdir(location_dir):
                        image_path = os.path.join(location_dir, image_name)
                        if os.path.isfile(image_path):
                            # Check if the image already exists in the database
                            existing_image = (
                                session.query(Image)
                                .filter_by(
                                    image_name=image_name, image_location=location
                                )
                                .first()
                            )
                            if not existing_image:
                                # Update the image URL to the new path
                                image_url = os.path.join(
                                    "data", "images", location, image_name
                                )
                                new_image = Image(
                                    image_name=image_name,
                                    image_location=location,
                                    image_url=image_url,
                                )
                                session.add(new_image)
                                new_image.created_at = datetime.now()
                                count += 1
                            else:
                                # Update existing image URL if it has changed
                                if existing_image.image_url != image_path:
                                    existing_image.image_url = os.path.join(
                                        "data", "images", location, image_name
                                    )
                                    count += 1
            if count > 0:
                logger.info(f"Total images updated: {count}")
                session.commit()
            else:
                logger.info("No new images or existing images updated")

    @staticmethod
    def get_image_bbox(image_path, region_name, confidence=0.7):

        screen_coords = pyautogui.locateOnScreen(
            image_path, minSearchTime=3, confidence=confidence
        )
        # for screen_coords in pyautogui.locateAllOnScreen(r"C:\Repositories\Dual Universe\Missions Dual
        # Universe\data\bbox_images\ORBITAL_HUD_LANDED.png"): screen_coords = screen_coords
        if screen_coords is not None:
            left, top, width, height = screen_coords
            right = left + width
            bottom = top + height
            center_x = left + width // 2
            center_y = top + height // 2
            pyautogui.moveTo(center_x, center_y)
            SearchAreaQuerySet.create_or_update_search_area(
                region_name,
                {
                    "left": int(left),
                    "top": int(top),
                    "right": int(right),
                    "bottom": int(bottom),
                    "center_x": int(center_x),
                    "center_y": int(center_y),
                },
            )
            return
        raise ValueError(f"region_name: {region_name} was not found in")

    def character_table(self):
        try:
            with Session(self.db_engine) as session:
                _Character = select(Character)
                results = session.exec(_Character).first()
        except Exception as exc:
            logger.error(f"Error loading table: {exc}")
        if isinstance(results, Character):
            logger.success("Character_table - OK")
        logger.debug("Character_table - Not Valid")

    def load_Character_table(self):
        logger.debug(f"Loading Character table NotImplemented")
        pass

    def load_MissionMetadata_table(self):
        logger.debug(f"Loading Mission metadata table NotImplemented")
        pass

    def main(self):
        db_table = DbChecker(engine, Image)
        if db_table.is_valid():
            print("Good")
        else:
            print("Bad")
        try:

            _Image = select(Image)
            results = session.exec(_Image).first()
            if isinstance(results, Image):
                logger.success(f"Image_table - OK")
            else:
                self.load_Image_table()

            _Mission = select(Mission)
            results = session.exec(_Mission).first()
            if isinstance(results, Mission):
                logger.success("Mission_table - OK")
            else:
                self.load_Mission_table()

            _MissionMetadata = select(MissionMetadata)
            results = session.exec(_MissionMetadata).first()
            if isinstance(results, MissionMetadata):
                logger.success("MissionMetadata_table - OK")
            else:
                self.load_MissionMetadata_table()

            _SearchArea = select(SearchArea)
            results = session.exec(_SearchArea).first()
            if isinstance(results, SearchArea):
                logger.success("SearchArea_table - OK")
            else:
                self.load_SearchArea_table()

        except Exception as e:
            logger.error(f"Error loading table: {e}")
            raise e
        else:
            self.load_image_entries_to_db()


if __name__ == "__main__":
    obj = DbConfig()
    obj.main()

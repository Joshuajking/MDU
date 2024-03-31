import ast
import datetime
import enum
import os
import uuid
from typing import Any, Tuple, Optional, Dict

from sqlalchemy import create_engine
from sqlmodel import Session, select

from config.config_manager import ConfigManager
from logs.logging_config import logger
from models.models import SearchArea, Character, Mission, Image, ImageLocation, MissionMetadata
from path_router import DirectoryPaths

config_manager = ConfigManager()
engine = create_engine(
	f"sqlite:///{os.path.join(DirectoryPaths.ROOT_DIR, config_manager.get_value('config.database'))}", echo=False)


class MissionMetaQuerySet:

	@classmethod
	def create_or_update_round_trips(cls, round_trip: int):
		with Session(engine) as session:
			metadata = session.query(MissionMetadata).filter_by(round_trips=round_trip).first()
			if metadata:
				session.query(MissionMetadata).filter_by(id=metadata.id).update(
					{"round_trips": metadata.round_trips + 1}
				)
			else:
				session.add(MissionMetadata(round_trips=1))

			session.commit()

	@classmethod
	def read_round_trips(cls) -> int:
		with Session(engine) as session:
			metadata = session.query(MissionMetadata).first()
			if metadata:
				return metadata.round_trips
			return 0  # Default value if no metadata is found


class SearchAreaQuerySet:

	@classmethod
	def select_searcharea(cls):
		with Session(engine) as session:
			return session.exec(select(SearchArea)).all()

	@classmethod
	def get_searcharea_by_name(cls, name: str):
		with Session(engine) as session:
			searcharea = session.exec(select(SearchArea).where(SearchArea.region_name == name)).first()
		searcharea.region = region
		return region

	@classmethod
	def create_or_update_search_area(cls, region_name: str, updates: Dict[str, int]):
		try:
			with Session(engine) as session:
				search_area = session.query(SearchArea).filter_by(region_name=region_name).first()
				if search_area:
					for key, value in updates.items():
						setattr(search_area, key, int(value))
					search_area.center_x = (search_area.left + search_area.right) // 2
					search_area.center_y = (search_area.top + search_area.bottom) // 2
					search_area.updated_at = datetime.datetime.now()
					session.commit()
					logger.success(f'Search area updated in the database: {region_name}')
				else:
					new_search_area = SearchArea(region_name=region_name, **updates)
					new_search_area.center_x = (new_search_area.left + new_search_area.right) // 2
					new_search_area.center_y = (new_search_area.top + new_search_area.bottom) // 2
					new_search_area.updated_at = datetime.datetime.now()
					session.add(new_search_area)
					session.commit()
					logger.success(f'New search area created in the database: {region_name}')
		except Exception as ex:
			logger.error(f"Could not update or create search area: {ex}")
			raise ValueError(f"Could not update or create search area: {ex}")

	@classmethod
	def create_search_area(cls, region_name: str, region_bbox: Tuple[int, int, int, int]):
		with Session(engine) as session:
			new_search_area = SearchArea(region_name=region_name, region_bbox_left=region_bbox[0],
			                             region_bbox_top=region_bbox[1], region_bbox_right=region_bbox[2],
			                             region_bbox_bottom=region_bbox[3])
			session.add(new_search_area)
			new_search_area.created_at = datetime.datetime.now()
			session.commit()
			print(f'New search area added to the database: {region_name}')

	@classmethod
	def read_search_area_by_name(cls, region_name: str) -> Optional['SearchArea']:
		with Session(engine) as session:
			search_area = session.query(SearchArea).filter_by(region_name=region_name).first()
			if search_area is not None:
				return search_area
			else:
				logger.info(f"Search area with name '{region_name}' not found.")
				return None

	@classmethod
	def update_search_area(cls, region_name: str, region_bbox: Tuple[int, int, int, int]):
		with Session(engine) as session:
			search_area = session.query(SearchArea).filter_by(region_name=region_name).first()
			if search_area:
				search_area.region_bbox = region_bbox
				search_area.updated_at = datetime.datetime.now()
				session.commit()
				print(f'Search area updated in the database: {region_name}')
			else:
				print("Search area not found")

	@classmethod
	def delete_search_area_by_name(cls, region_name: str):
		with Session(engine) as session:
			search_area = session.query(SearchArea).filter_by(region_name=region_name).first()
			if search_area:
				session.delete(search_area)
				session.commit()
				print(f'Search area deleted: {region_name}')
			else:
				print("Search area not found")


class ImageQuerySet:
	@classmethod
	def get_all_images(cls):
		try:
			with Session(engine) as session:
				image = session.query(Image).all()
		except Exception as e:
			logger.error(f"{str(e)}")
		return image

	@classmethod
	def get_all_image_by_location(cls, image_location: enum.Enum | str):
		with Session(engine) as session:
			statement = select(Image).where(Image.image_location == image_location)
			result = session.exec(statement)
			image = result.all()
			return image


	@classmethod
	def create_or_update_image(cls, image_name: str, image_location: str):
		image_path = os.path.join(image_location, image_name)
		parts = image_name.split(".")
		if len(parts) > 1:
			extension = parts[-1]
			if extension != "png":
				raise ValueError("File must have a .png extension")
		else:
			image_name += ".png"
		with Session(engine) as session:
			image = session.query(Image).filter_by(image_name=image_name).first()
			if image:
				image.image_location = image_location
				image.image_url = image_path
				session.commit()
				print(f'Image updated in the database: {image_name}')
			else:
				if os.path.isfile(image_path):
					new_image = Image(image_name=image_name, image_location=image_location, image_url=image_path)
					session.add(new_image)
					session.commit()
					print(f'New image added to the database: {image_name}')
				else:
					print(f'Image not found: {image_name}')

	@classmethod
	def create_image(cls, image_name: str, image_location: str):
		image_path = os.path.join(image_location, image_name)
		if os.path.isfile(image_path):
			with Session(engine) as session:
				new_image = Image(
					image_name=image_name,
					image_location=image_location,
					image_url=image_path,
					image_bbox_left=0,
					image_bbox_top=0,
					image_bbox_right=0,
					image_bbox_bottom=0,
					image_bbox_center_x=0,
					image_bbox_center_y=0
				)
				session.add(new_image)
				session.commit()
				print(f'New image added to the database: {image_name}')
		else:
			print(f'Image not found: {image_name}')

	@classmethod
	def get_images_by_field(cls, field_name: str):
		"""
		:param field_name:
		:return:
		"""
		with Session(engine) as session:
			images = session.exec(select(cls).where(getattr(cls, Image.image_location) == field_name)).all()
			return images

	@classmethod
	def read_image_by_name(cls, image_name: str, image_location: Optional[ImageLocation]) -> Optional['Image']:
		try:
			parts = image_name.split(".")
			if len(parts) > 1:
				extension = parts[-1]
				if extension != "png":
					raise ValueError("File must have a .png extension")
			else:
				image_name += ".png"
			with Session(engine) as session:
				image = session.query(Image).filter_by(image_name=image_name, image_location=image_location).first()
				if image:
					region = image.region
					if region is not None:
						region = tuple(map(int, ast.literal_eval(region)))
						image.region = region
		except Exception as e:
			logger.error(e)
		return image

	@classmethod
	def update_image_by_id(cls, id: uuid.uuid4, updates: Dict[str, Any]):

		with Session(engine) as session:
			image = session.query(Image).filter_by(id=id).first()
			if image:
				try:
					for field, value in updates.items():
						setattr(image, field, value)
					image.updated_at = datetime.datetime.now()  # Set updated_at field
					session.commit()
					print(f'Image updated in the database: {id}')
					return True
				except Exception as e:
					session.rollback()  # Rollback changes if an error occurs
					print(f'Error updating image: {e}')
			else:
				print("Image not found")

		return False

	@classmethod
	def delete_image_by_name(cls, image_name: str):
		with Session(engine) as session:
			image = session.query(Image).filter_by(image_name=image_name).first()
			if image:
				session.delete(image)
				session.commit()
				print(f'Image deleted: {image_name}')
			else:
				print("Image not found")

	@classmethod
	def delete_image_by_id(cls, id: uuid.uuid4):
		with Session(engine) as session:
			image = session.query(Image).filter_by(id=id).first()
			if image:
				session.delete(image)
				session.commit()
				print(f'Image deleted: {image.image_name}')
			else:
				print("Image not found")


class CharacterQuerySet:

	@classmethod
	def create_or_update_character(cls, username: str, email: str, password: str, has_package: bool,
	                               has_gametime: bool):
		with Session(engine) as session:
			character = session.query(Character).filter_by(username=username).first()
			if character:
				character.email = email
				character.password = password
				character.has_package = has_package
				character.has_gametime = has_gametime
				session.commit()
				print(f'Character updated in the database: {username}')
			else:
				new_character = Character(username=username, email=email, password=password, has_package=has_package,
				                          has_gametime=has_gametime)
				session.add(new_character)
				session.commit()
				print(f'New character added to the database: {username}')

	@classmethod
	def create_character(cls, username: str, email: str, password: str, has_package: bool, has_gametime: bool):
		with Session(engine) as session:
			new_character = Character(username=username, email=email, password=password, has_package=has_package,
			                          has_gametime=has_gametime)
			session.add(new_character)
			session.commit()
			print(f'New character added to the database: {username}')

	@classmethod
	def select_all_characters(cls):
		with Session(engine) as session:
			characters = session.query(Character).all()
			return characters

	@classmethod
	def count_active_characters(cls):
		with Session(engine) as session:
			characters = session.query(Character).filter(Character.active == True).count()
			return characters

	@classmethod
	def get_active_characters(cls):
		with Session(engine) as session:
			characters = session.query(Character).filter(Character.active == True).all()
			return characters

	@classmethod
	def count_has_package_characters(cls):
		with Session(engine) as session:
			characters = session.query(Character).filter(Character.has_package == True).count()
			return characters

	@classmethod
	def count_has_package_and_active_characters(cls):
		with Session(engine) as session:
			# Query to count active characters that have a package
			count = session.query(Character).filter(Character.active == True, Character.has_package == True).count()
		return count

	@classmethod
	def get_has_package_characters(cls):
		with Session(engine) as session:
			characters = session.query(Character).filter(Character.has_package == True).all()
			return characters

	@classmethod
	def read_character_by_username(cls, username: str) -> Optional['Character']:
		with Session(engine) as session:
			character = session.query(Character).filter_by(username=username).first()
			return character

	@classmethod
	def update_character(cls, obj, updates: Dict[str, Any]):
		with Session(engine) as session:
			character = session.query(Character).filter_by(id=obj.id).first()
			if character:
				for key, value in updates.items():
					setattr(character, key, value)
				character.updated_at = datetime.datetime.now()
				session.commit()
				logger.success(f"Updated character: {obj.username} - {updates}")
				return
			else:
				logger.error("Character not found")
				raise KeyError(f'Character not found')

	@classmethod
	def delete_character_by_username(cls, username: str):
		with Session(engine) as session:
			character = session.query(Character).filter_by(username=username).first()
			if character:
				session.delete(character)
				session.commit()
				print(f'Character deleted: {username}')
			else:
				print("Character not found")


class MissionQuerySet:
	@classmethod
	def read_mission_by_title(cls, title: str) -> Optional['Mission']:
		"""
		Read mission by title
		:param title:
		:return:
		"""
		with Session(engine) as session:
			mission = session.query(Mission).filter_by(title=title).first()
			return mission

	@classmethod
	def update_mission(cls, title: str, updates: Dict[str, Any]):
		with Session(engine) as session:
			mission = session.query(Mission).filter_by(title=title).first()
			if mission:
				for key, value in updates.items():
					setattr(mission, key, value)
				mission.updated_at = datetime.datetime.now()
				session.commit()
				print(f'Mission updated in the database: {title}')
				return True
			else:
				# Create a new mission if not found
				new_mission = Mission(title=title, **updates, created_at=datetime.datetime.now(),
				                      updated_at=datetime.datetime.now())
				session.add(new_mission)
				session.commit()
				print(f'New mission created in the database: {title}')
				return True

	@classmethod
	def delete_mission_by_title(cls, title: str):
		with Session(engine) as session:
			mission = session.query(Mission).filter_by(title=title).first()
			if mission:
				session.delete(mission)
				session.commit()
				print(f"Mission deleted: {title}")
			else:
				print("Mission not found")

	@classmethod
	def create_or_update_mission(cls, update_dict: dict[str, Any]) -> None:
		title = update_dict.pop('title', None)  # Remove 'title' from update_dict if present
		if not title:
			raise ValueError("Title is required for creating or updating a mission.")

		with Session(engine) as session:
			existing_mission = session.exec(select(Mission).where(Mission.title == title)).first()

			if not existing_mission:
				new_mission = Mission(title=title, **update_dict)
				session.add(new_mission)
				session.commit()
				logger.info(f'New mission added to the database: {title}')
			else:
				for key, value in update_dict.items():
					setattr(existing_mission, key, value)
				session.commit()
				logger.info(f'Mission updated in the database: {title}')


if __name__ == '__main__':
	sa_obj = SearchAreaQuerySet()
	val = sa_obj.select_searcharea()
	print(val)

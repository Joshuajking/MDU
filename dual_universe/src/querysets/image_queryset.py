import ast
import datetime
import enum
import os
import uuid
from typing import Optional, Dict, Any

from loguru import logger
from sqlmodel import Session, select

from dual_universe.src.models.image_model import Image, ImageLocation, get_enum_value

from dual_universe.settings import db_engine as engine


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
                print(f"Image updated in the database: {image_name}")
            else:
                if os.path.isfile(image_path):
                    new_image = Image(
                        image_name=image_name,
                        image_location=image_location,
                        image_url=image_path,
                    )
                    session.add(new_image)
                    session.commit()
                    print(f"New image added to the database: {image_name}")
                else:
                    print(f"Image not found: {image_name}")

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
                    image_bbox_center_y=0,
                )
                session.add(new_image)
                session.commit()
                print(f"New image added to the database: {image_name}")
        else:
            print(f"Image not found: {image_name}")

    @classmethod
    def get_images_by_field(cls, field_name: str):
        """
        :param field_name:
        :return:
        """
        with Session(engine) as session:
            images = session.exec(
                select(cls).where(getattr(cls, Image.image_location) == field_name)
            ).all()
            return images

    @classmethod
    def read_image_by_name(
        cls, image_name: str, image_location: Optional[ImageLocation]
    ) -> Optional["Image"]:
        try:
            # Convert image_location from string to ImageLocation Enum if it's a string
            if isinstance(image_location, str):
                image_location = get_enum_value(ImageLocation, image_location)

            parts = image_name.split(".")
            if len(parts) > 1:
                extension = parts[-1]
                if extension != "png":
                    raise ValueError("File must have a .png extension")
            else:
                image_name += ".png"
            with Session(engine) as session:
                image = (
                    session.query(Image)
                    .filter_by(image_name=image_name, image_location=image_location)
                    .first()
                )
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
                    print(f"Image updated in the database: {id}")
                    return True
                except Exception as e:
                    session.rollback()  # Rollback changes if an error occurs
                    print(f"Error updating image: {e}")
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
                print(f"Image deleted: {image_name}")
            else:
                print("Image not found")

    @classmethod
    def delete_image_by_id(cls, id: uuid.uuid4):
        with Session(engine) as session:
            image = session.query(Image).filter_by(id=id).first()
            if image:
                session.delete(image)
                session.commit()
                print(f"Image deleted: {image.image_name}")
            else:
                print("Image not found")

import datetime
from typing import Optional, Dict, Any

from loguru import logger
from sqlmodel import Session

from dual_universe.src.models.character_model import Character
from dual_universe.settings import db_engine as engine


class CharacterQuerySet:

    @classmethod
    def create_or_update_character(
        cls,
        username: str,
        email: str,
        password: str,
        has_package: bool,
        has_gametime: bool,
    ):
        with Session(engine) as session:
            character = session.query(Character).filter_by(username=username).first()
            if character:
                character.email = email
                character.password = password
                character.has_package = has_package
                character.has_gametime = has_gametime
                session.commit()
                print(f"Character updated in the database: {username}")
            else:
                new_character = Character(
                    username=username,
                    email=email,
                    password=password,
                    has_package=has_package,
                    has_gametime=has_gametime,
                )
                session.add(new_character)
                session.commit()
                print(f"New character added to the database: {username}")

    @classmethod
    def create_character(
        cls,
        username: str,
        email: str,
        password: str,
        has_package: bool,
        has_gametime: bool,
    ):
        with Session(engine) as session:
            new_character = Character(
                username=username,
                email=email,
                password=password,
                has_package=has_package,
                has_gametime=has_gametime,
            )
            session.add(new_character)
            session.commit()
            print(f"New character added to the database: {username}")

    @classmethod
    def select_all_characters(cls):
        with Session(engine) as session:
            characters = session.query(Character).all()
            return characters

    @classmethod
    def count_active_characters(cls):
        with Session(engine) as session:
            characters = (
                session.query(Character).filter(Character.active == True).count()
            )
            return characters

    @classmethod
    def get_active_characters(cls):
        with Session(engine) as session:
            characters = session.query(Character).filter(Character.active == True).all()
            return characters

    @classmethod
    def count_has_package_characters(cls):
        with Session(engine) as session:
            characters = (
                session.query(Character).filter(Character.has_package == True).count()
            )
            return characters

    @classmethod
    def count_has_package_and_active_characters(cls):
        with Session(engine) as session:
            # Query to count active characters that have a package
            count = (
                session.query(Character)
                .filter(Character.active == True, Character.has_package == True)
                .count()
            )
        logger.info(f"package_count: {count}")
        return count

    @classmethod
    def get_has_package_characters(cls):
        with Session(engine) as session:
            characters = (
                session.query(Character).filter(Character.has_package == True).all()
            )
            return characters

    @classmethod
    def read_character_by_username(cls, username: str) -> Optional["Character"]:
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
                raise KeyError(f"Character not found")

    @classmethod
    def delete_character_by_username(cls, username: str):
        with Session(engine) as session:
            character = session.query(Character).filter_by(username=username).first()
            if character:
                session.delete(character)
                session.commit()
                print(f"Character deleted: {username}")
            else:
                print("Character not found")

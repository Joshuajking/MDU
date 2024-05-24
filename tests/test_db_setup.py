import unittest
import uuid
from unittest.mock import patch, MagicMock

from loguru import logger

from src.db_setup import DbConfig
from src.models import *
from sqlalchemy import create_engine, inspect
from faker import Faker

from sqlmodel import SQLModel, Session, select


class TestDBSetup(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        SQLModel.metadata.create_all(self.engine)
        self.db_config = DbConfig(self.engine)

    def tearDown(self):
        pass

    def test_Character_table_exists(self):
        # Assuming self.engine is your SQLAlchemy engine
        with Session(self.engine) as session:
            inspector = inspect(session.connection())
            table_names = inspector.get_table_names()

        self.assertIn("character", table_names)
        logger.info('TestDBSetup.test_Character_table_exists')

    def test_Image_table_exists(self):
        # Assuming self.engine is your SQLAlchemy engine
        with Session(self.engine) as session:
            inspector = inspect(session.connection())
            table_names = inspector.get_table_names()

        self.assertIn("image", table_names)
        logger.info('TestDBSetup.test_Image_table_exists')

    def test_Mission_table_exists(self):
        # Assuming self.engine is your SQLAlchemy engine
        with Session(self.engine) as session:
            inspector = inspect(session.connection())
            table_names = inspector.get_table_names()

        self.assertIn("mission", table_names)
        logger.info('TestDBSetup.test_Mission_table_exists')

    def test_MissionMetadata_table_exists(self):
        # Assuming self.engine is your SQLAlchemy engine
        with Session(self.engine) as session:
            inspector = inspect(session.connection())
            table_names = inspector.get_table_names()

        self.assertIn("missionmetadata", table_names)
        logger.info('TestDBSetup.test_MissionMetadata_table_exists')

    def test_SearchArea_table_exists(self):
        # Assuming self.engine is your SQLAlchemy engine
        with Session(self.engine) as session:
            inspector = inspect(session.connection())
            table_names = inspector.get_table_names()

        self.assertIn("searcharea", table_names)
        logger.info('TestDBSetup.test_SearchArea_table_exists')

    @unittest.skip("TestDBSetup.test_load_Character_table")
    def test_load_Character_table(self):
        self.db_config.load_Character_table()
        with Session(self.engine) as session:
            _Character = select(Character)
            results = session.exec(_Character).first()

        self.assertIsInstance(results, Character)
        logger.info('TestDBSetup.test_load_Character_table')

    def test_load_Image_table(self):
        self.db_config.load_Image_table()
        with Session(self.engine) as session:
            _Image = select(Image)
            results = session.exec(_Image).first()

        self.assertTrue(results is not None)
        logger.info('TestDBSetup.test_load_Image_table')

    @unittest.skip("TestDBSetup.test_load_Mission_table")
    def test_load_Mission_table(self):
        self.db_config.load_Mission_table()
        with Session(self.engine) as session:
            _Mission = select(Mission)
            results = session.exec(_Mission).first()

        self.assertTrue(results is not None)
        logger.info('TestDBSetup.test_load_Mission_table')

    @unittest.skip("TestDBSetup.test_load_MissionMetadata_table")
    def test_load_MissionMetadata_table(self):
        self.db_config.load_MissionMetadata_table()
        with Session(self.engine) as session:
            _MissionMetadata = select(MissionMetadata)
            results = session.exec(_MissionMetadata).first()

        self.assertTrue(results is not None)
        logger.info('TestDBSetup.test_load_MissionMetadata_table')

    def test_load_SearchArea_table(self):
        self.db_config.load_SearchArea_table()
        with Session(self.engine) as session:
            _SearchArea = select(SearchArea)
            results = session.exec(_SearchArea).first()

        self.assertTrue(results is not None)
        logger.info('TestDBSetup.test_load_SearchArea_table')

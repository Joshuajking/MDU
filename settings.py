import os

from decouple import config
from sqlalchemy import create_engine

from router import DirectoryPaths
from src.config_manager import ConfigManager

config_manager = ConfigManager()

DATABASE_URL = config('DATABASE_URL')
engine = create_engine(f"sqlite:///{os.path.join(DirectoryPaths.ROOT_DIR, DATABASE_URL)}", echo=False)

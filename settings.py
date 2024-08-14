import os

from decouple import config
from sqlalchemy import create_engine

from router import DirectoryPaths
from src.config_manager import ConfigManagerMixin

config_manager = ConfigManagerMixin()

DATABASE_URL = config("DATABASE_URL")
engine = create_engine(
    f"sqlite:///{os.path.join(DirectoryPaths.ROOT_DIR, DATABASE_URL)}", echo=False
)

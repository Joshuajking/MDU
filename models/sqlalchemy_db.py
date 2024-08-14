import os

from sqlalchemy import create_engine
from config.config_manager import ConfigManager
from path_router import DirectoryPaths


def connect_to_db():
    # Database URL
    config_manager = ConfigManager()
    engine = create_engine(
        f"sqlite:///{os.path.join(DirectoryPaths.MODEL_DIR, config_manager.get_value('config.database'))}",
        echo=True,
    )
    return engine

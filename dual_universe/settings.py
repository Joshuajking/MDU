import os
from pathlib import Path

from sqlalchemy import create_engine


ROOT_DIR = Path(__file__).resolve().parent

CONFIG_DIR = ROOT_DIR / "config"
ASSETS_DIR = ROOT_DIR / "assets"
# JSON_DIR = DATA_DIR / "json"
LOGS_DIR = ROOT_DIR / "logs"
CORES_DIR = ROOT_DIR / "src"
DOCS_DIR = ROOT_DIR / "docs"
# GUI_DIR = ROOT_DIR / "ui"
MODEL_DIR = ROOT_DIR / "models"
# BACKUP_DB_DIR = ROOT_DIR / "db_backup"
TEMP_DIR = ROOT_DIR / "temp"
OCR_ENHANCED_DIR = TEMP_DIR / "ocr_enhanced_images"
TEMPLATES_DIR = ROOT_DIR / "templates"
INVALID_IMAGES_DIR = TEMPLATES_DIR / "invalid_images"
TESTS_DIR = ROOT_DIR / "tests"
# UI_DIR = ROOT_DIR / "ui"
UTILS_DIR = ROOT_DIR / "utils"
DU_IMAGES_DIR = ASSETS_DIR / "images"
SEARCH_AREA_DIR = ASSETS_DIR / "search_areas"

# Example of creating the directories if they don't exist
# for directory in [
#     CONFIG_DIR,
#     ASSETS_DIR,
#     LOGS_DIR,
#     CORES_DIR,
#     DOCS_DIR,
#     MODEL_DIR,
#     TEMP_DIR,
#     OCR_ENHANCED_DIR,
#     TEMPLATES_DIR,
#     INVALID_IMAGES_DIR,
#     TESTS_DIR,
#     UTILS_DIR,
#     DU_IMAGES_DIR,
#     SEARCH_AREA_DIR,
# ]:
#     directory.mkdir(parents=True, exist_ok=True)


engine = create_engine(
    f"sqlite:///dual_universe.db",
    echo=True,
)

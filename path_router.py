from pathlib import Path


class DirectoryPaths:
    ROOT_DIR = Path(__file__).resolve().parent

    CONFIG_DIR = ROOT_DIR / "config"
    DATA_DIR = ROOT_DIR / "data"
    JSON_DIR = DATA_DIR / "json"
    LOGS_DIR = ROOT_DIR / "logs"
    CORES_DIR = ROOT_DIR / "core"
    DOCS_DIR = ROOT_DIR / "docs"
    GUI_DIR = ROOT_DIR / "ui"
    MODEL_DIR = ROOT_DIR / "models"
    BACKUP_DB_DIR = ROOT_DIR / "db_backup"
    TEMP_DIR = ROOT_DIR / "temp"
    OCR_ENHANCED_DIR = TEMP_DIR / "ocr_enhanced_images"
    TEMPLATES_DIR = ROOT_DIR / "templates"
    INVALID_IMAGES_DIR = TEMPLATES_DIR / "invalid_images"
    TESTS_DIR = ROOT_DIR / "tests"
    UI_DIR = ROOT_DIR / "ui"
    UTILS_DIR = ROOT_DIR / "utils"
    DU_IMAGES_DIR = DATA_DIR / "du_images"
    SEARCH_AREA_DIR = DATA_DIR / "search_areas"

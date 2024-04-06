from pathlib import Path


class DirectoryPaths:
	ROOT_DIR = Path(__file__).resolve().parent

	SRC_DIR = ROOT_DIR / 'src'
	DATA_DIR = ROOT_DIR / 'data'
	LOGS_DIR = ROOT_DIR / 'logs'
	DOCS_DIR = ROOT_DIR / 'docs'
	TEMP_DIR = SRC_DIR / 'temp'
	TESTS_DIR = ROOT_DIR / 'tests'
	UTILS_DIR = SRC_DIR / 'utils'
	DU_IMAGES_DIR = DATA_DIR / 'du_images'
	SEARCH_AREA_DIR = DATA_DIR / 'bbox_images'
	DB_DUMP_DIR = DATA_DIR / 'db_dump_files'


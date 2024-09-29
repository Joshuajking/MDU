import json
import os

from dual_universe.settings import ASSETS_DIR
from dual_universe.logs.logging_config import logger


def read_json(json_file) -> json:
    """
    :param json_file:
    :return:
    """

    # read_file_path = os.path.join(ASSETS_DIR, json_file)
    data = None

    try:
        # Check if the file is empty
        if os.path.getsize(read_file_path) > 0:
            with open(read_file_path, "r") as _json_file:
                data = json.load(_json_file)
        else:
            logger.warning(f"The JSON file is empty: {read_file_path}")
    except json.JSONDecodeError as e:
        logger.warning(f"Error decoding JSON: {e}")
    except FileNotFoundError:
        logger.warning(f"File not found: {read_file_path}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
    logger.debug(f"Read JSON: {read_file_path}")
    return data


def write_json(**kwargs):
    """
    :param json_file
    :param json_data
    :return:
    """
    json_file = kwargs.get("json_file")
    data = kwargs.get("json_data")
    write_file_path = os.path.join(DirectoryPaths.JSON_DIR, json_file)
    try:
        with open(write_file_path, "w") as _json_file:
            json.dump(data, _json_file, indent=4)
    except Exception as e:
        logger.warning(f"{e}")
    logger.debug(f"WRITTEN: {data}: {write_file_path}")


def is_package(**kwargs):
    progress_file_path = "character_progress.json"
    json_file = os.path.join(DirectoryPaths.JSON_DIR, progress_file_path)

    username = kwargs.get("username")
    has_package = kwargs.get("has_package")
    has_game_time = kwargs.get("has_game_time")
    progress_data = read_json(json_file=json_file)

    character_data = progress_data["characters"].get(username, {})
    _has_package = character_data["has_package"]
    _has_game_time = character_data["has_game_time"]
    # Check if has_package and has_game_time are explicitly set to 1
    if kwargs.get("has_package", _has_package) == 1:
        character_data["has_package"] = 1
    if kwargs.get("has_game_time", _has_game_time) == 1:
        character_data["has_game_time"] = 1

    # If has_package and has_game_time are not explicitly set to 1, default to 0
    if kwargs.get("has_package", _has_package) != 1:
        character_data["has_package"] = 0
    if kwargs.get("has_game_time", _has_game_time) != 1:
        character_data["has_game_time"] = 0

    progress_data["characters"][username] = character_data
    __has_package = character_data["has_package"]
    __has_game_time = character_data["has_game_time"]

    try:
        with open(json_file, "w") as progress_file:
            json.dump(progress_data, progress_file, indent=4)
    except Exception as e:
        logger.warning(f"{e}")
    logger.info(
        f"UPDATED: {username} -- has_package: {__has_package} - has_game_time: {__has_game_time}"
    )
    return


if __name__ == "__main__":
    pass

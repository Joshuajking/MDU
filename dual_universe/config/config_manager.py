import json
import os
import time

from dual_universe.logs.logging_config import logger
from dual_universe.settings import ROOT_DIR


class ConfigMixin:
    def __init__(self):
        self.json_config_path = os.path.join(ROOT_DIR, "config.json")
        self.config_data = self.load_config()

    def load_config(self):
        try:
            with open(self.json_config_path, "r", encoding="utf-8") as config_file:
                data = json.load(config_file)
                return data
        except FileNotFoundError:
            logger.error(f"Config file not found at {self.json_config_path}")
            raise FileNotFoundError(f"Config file not found at {self.json_config_path}")
        except json.JSONDecodeError:
            logger.error(
                f"Invalid JSON format in config file at {self.json_config_path}"
            )
            raise ValueError(
                f"Invalid JSON format in config file at {self.json_config_path}"
            )

    def get_value(self, key):
        keys = key.split(".")
        data = self.config_data
        try:
            for k in keys:
                data = data.get(k)
                if data is None:
                    break
        except Exception as e:
            logger.error(f"{str(e)} in config file at {self}")
        # print(f"Key: {key}, Value: {data}")
        return data


def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        # print(f"{func.__name__} execution time: {execution_time} seconds")
        logger.info(f"{func.__name__} execution time: {execution_time} seconds")
        return result

    return wrapper

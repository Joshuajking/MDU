from time import sleep, perf_counter

from loguru import logger

from config.config_manager import ConfigManager
from utils.read_json import read_json, is_package

config_manager = ConfigManager()
character_list = config_manager.get_value('config.character_list')
app_path = config_manager.get_value('config.app_path')


# TODO want to incorprate this into the start and ask for user input


def character_link():
    """

    :return:
    """

    character_progress = read_json(config_manager.get_value('config.character_progress'))  # Get the characters dictionary
    # loop over all the accounts
    for username, character_info in character_progress['characters'].items():
        email = character_info.get('email')
        password = character_info.get('pwd')
        logger.info(f'Attempting login: {email}')

        character_time_start = perf_counter()
        login_character_result = login_character(username=username, email=email, password=password)

        if login_character_result['status'] == 'nogameTime':
            is_package(has_game_time=0, username=username)
            continue

        elif login_character_result['status'] == 'loggedIn':
            logout(respawn=False)
            character_time_stop = perf_counter()
            logger.info(f'character_timing: {character_time_stop - character_time_start}')
            continue

        elif login_character_result['status'] == 'successfulLogin':
            result = char_check()
            has_package = result.get('has_package')

            is_package(has_game_time=1, has_package=has_package, username=username)

            sleep(config_manager.get_value('config.char_sleep_time'))

            logout(respawn=False)

        character_time_stop = perf_counter()
        logger.info(f'character_link_timing: {character_time_stop - character_time_start}')

        continue


if __name__ == "__main__":
    character_link()

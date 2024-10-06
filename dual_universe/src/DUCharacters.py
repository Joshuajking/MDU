import sys

import pyautogui

from dual_universe.config.config_manager import timing_decorator
from dual_universe.config.db_setup import EncryptPassword
from dual_universe.integrations.key_board import keyboard_press, keyboard_write
from dual_universe.integrations.pydirect_input import pydirectinput_press
from dual_universe.logs.logging_config import logger
from dual_universe.src.error_validation import BatchErrorValidation
from dual_universe.src.querysets.character_queryset import CharacterQuerySet
from dual_universe.src.verify_screen import VerifyScreenMixin


class DUCharacters:
    def __init__(
        self,
        screen_mixin=VerifyScreenMixin,
        batch_validation=BatchErrorValidation,
        char=CharacterQuerySet,
        keyboard=keyboard_press,
        write=keyboard_write,
        encrypt=EncryptPassword,
    ):
        self.screen_mixin = screen_mixin
        self.batch_validation = batch_validation()
        self.keyboard = keyboard
        self.write = write
        self.encrypt = encrypt()
        self.char = char
        self.character = None

    @staticmethod
    def _clear_input_login_fields():
        logger.info("Clearing input login fields...")
        keyboard_press("tab")
        keyboard_press("backspace")
        keyboard_press("tab")
        keyboard_press("backspace")

    def _is_email_field_empty(self):
        logger.info("Checking if email is empty...")
        is_email_field_empty = self.screen_mixin(
            screen_name="ImageLocation.LOGIN_SCREEN",
            image_to_compare="email_login",
            mouse_click=True,
            mouse_clicks=1,
        )
        if is_email_field_empty.request.status_code == 200:
            # checking if email field is empty
            keyboard_write(self.character.email)
            keyboard_press("tab")
            ...
        return is_email_field_empty

    def _is_password_field_empty(self):
        logger.info("Checking if password is empty...")
        is_password_field_empty = self.screen_mixin(
            screen_name="ImageLocation.LOGIN_SCREEN",
            image_to_compare="password_login",
            mouse_click=True,
            mouse_clicks=1,
            skip_sleep=True,
        )
        if is_password_field_empty.request.status_code == 200:
            decrypt = EncryptPassword()
            keyboard_write(decrypt.decrypt_password(self.character.password))
            keyboard_press("enter")
            ...
        return is_password_field_empty

    def _validate_loading(self):
        is_loading_complete = self.screen_mixin(
            screen_name="ImageLocation.IN_GAME_SCREEN",
            image_to_compare="loading_complete",
            minSearchTime=120,
        )
        # checking if character loaded in game within minSearchTime
        if not is_loading_complete.request.status_code == 200:
            logger.warning("Loading in game failed")
            sys.exit(0)  # ToDo: if game failed to load restart game?

    def login(self, character):
        self.character = character

        count = 0
        attempts = 4
        while count < attempts:
            self._clear_input_login_fields()

            result_is_email_field_empty = self._is_email_field_empty()
            if result_is_email_field_empty.request.status_code == 400:
                count += 1
                continue

            result_is_password_field_empty = self._is_password_field_empty()
            if result_is_password_field_empty.request.status_code == 400:
                count += 1
                continue

            results = self.batch_validation.validate_errors()

            # Handle results further if needed
            for result, code in results.items():
                if code == 400:
                    logger.success(f"No {result} found.")
                    if result == "gametime_error":
                        CharacterQuerySet.update_character(
                            self.character, {"has_gametime": True}
                        )
                elif code == 200:
                    logger.warning(f"{result} found.")
                    if result == "gametime_error":
                        logger.debug(f"No game time: {self.character.username}")
                        CharacterQuerySet.update_character(
                            self.character, {"has_gametime": False, "active": False}
                        )
                        return
                    break
            if code == 200:
                continue
            break

        self._validate_loading()

        logger.success(f"{self.character.username} Successfully loaded game")
        self.survey()
        self.welcome_reward()
        return True

    def logout(self, respawn=False):
        loading_complete_response = self.screen_mixin(
            screen_name="ImageLocation.IN_GAME_SCREEN",
            image_to_compare="loading_complete",
            skip_sleep=True,
        )
        if loading_complete_response.request.status_code == 400:
            return

        count = 0
        max_count = 5
        at_esc_menu = False
        while not at_esc_menu:
            if count >= max_count:
                break

            pydirectinput_press("esc")
            logout_btn_response = self.screen_mixin(
                screen_name="ImageLocation.LOGOUT_SCREEN",
                image_to_compare="logout_btn",
                skip_sleep=True,
                mouse_click=True,
                mouse_clicks=1,
            )
            if not logout_btn_response.request.status_code == 200:
                count += 1
                pydirectinput_press("esc")
                continue
            break

    def check_location(self):  # TODO: Implement
        """Comes in after welcome back reward"""
        step_scroll = 1000
        # Press F4(map)
        keyboard_press("f4")
        # wait for map loading
        my_marker = VerifyScreenMixin(
            screen_name="ImageLocation.MAP_SCREEN",
            image_to_compare="my_map_marker",
            confidence=0.8,
        )
        # scroll-in(zoom)
        pyautogui.scroll(step_scroll, my_marker)
        # find planet info
        planet_label = VerifyScreenMixin(
            screen_name="ImageLocation.MAP_SCREEN",
            image_to_compare="map_planet_label",
            confidence=0.8,
        )
        # find Market icon
        market_icon = VerifyScreenMixin(
            screen_name="ImageLocation.MAP_SCREEN",
            image_to_compare="map_market_icon",
            confidence=0.8,
        )
        # VerifyScreen Market location
        market_label = VerifyScreenMixin(
            screen_name="ImageLocation.MAP_SCREEN",
            image_to_compare="map_market_label",
            confidence=0.8,
        )
        # close map (Esc)
        keyboard_press("esc")

    @timing_decorator
    def survey(self):
        survey = self.screen_mixin(
            screen_name="ImageLocation.IN_GAME_SCREEN",
            image_to_compare="survey",
            skip_sleep=True,
        )
        if survey.request.status_code == 200:
            self.screen_mixin(
                screen_name="ImageLocation.IN_GAME_SCREEN",
                image_to_compare="survey_skip_btn",
                mouse_click=True,
            )
        return

    @timing_decorator
    def welcome_reward(self):
        """Checks for Daily reward"""
        welcome_screen = self.screen_mixin(
            screen_name="ImageLocation.IN_GAME_SCREEN",
            image_to_compare="quanta_lable",
            skip_sleep=True,
        )
        if welcome_screen.request.status_code == 200:
            self.screen_mixin(
                screen_name="ImageLocation.IN_GAME_SCREEN",
                image_to_compare="selected_ok_btn",
                mouse_click=True,
            )
        return


if __name__ == "__main__":
    pass

import threading

import pyautogui

from dual_universe.config.config_manager import timing_decorator
from dual_universe.config.db_setup import EncryptPassword
from dual_universe.integrations.key_board import keyboard_press, keyboard_write
from dual_universe.integrations.pydirect_input import pydirectinput_press
from dual_universe.logs.logging_config import logger
from dual_universe.src.querysets.character_queryset import CharacterQuerySet
from dual_universe.src.verify_screen import VerifyScreenMixin


class DUCharacters:
    def __init__(
        self,
        screen_mixin=VerifyScreenMixin,
        char=CharacterQuerySet,
        keyboard=keyboard_press,
        write=keyboard_write,
        encrypt=EncryptPassword,
    ):
        self.screen_mixin = screen_mixin
        self.keyboard = keyboard
        self.write = write
        self.encrypt = encrypt()
        self.char = char
        self.character = None

    @staticmethod
    def _clear_input_login_fields():
        print("Clearing input login fields...")
        keyboard_press("tab")
        keyboard_press("backspace")
        keyboard_press("tab")
        keyboard_press("backspace")

    def _is_email_field_empty(self):
        print("Checking if email is empty...")
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
        return is_email_field_empty

    def _is_password_field_empty(self):
        print("Checking if password is empty...")
        is_password_field_empty = self.screen_mixin(
            screen_name="ImageLocation.LOGIN_SCREEN",
            image_to_compare="password_login",
            mouse_click=True,
            mouse_clicks=1,
            skip_sleep=True,
        )
        print(is_password_field_empty)
        if is_password_field_empty.request.status_code == 200:
            decrypt = EncryptPassword()
            keyboard_write(decrypt.decrypt_password(self.character.password))
            keyboard_press("enter")
        return is_password_field_empty

    def _validate_internal_error(self):
        is_internal_error = self.screen_mixin(
            screen_name="ImageLocation.LOGIN_SCREEN",
            image_to_compare="internal_error",
            confidence=0.8,
            skip_sleep=True,
        )
        # checking if there is an internal error (incorrect email or password)
        return is_internal_error.request.status_code

    def _validate_gametime(self):
        # this one is tricky, we want to see a 400 code to indicate that there was no game time error
        is_gametime_error = self.screen_mixin(
            screen_name="ImageLocation.LOGIN_SCREEN",
            image_to_compare="gametime_error_lable",
            skip_sleep=True,
        )
        return is_gametime_error.request.status_code

    def _validate_email(self):
        # this one is tricky, we want to see a 400 code to indicate that there was no game time error
        is_email_error = self.screen_mixin(
            screen_name="ImageLocation.LOGIN_SCREEN",
            image_to_compare="invalid_email",
            skip_sleep=True,
        )
        return is_email_error.request.status_code

    def _validate_server(self):
        # this one is tricky, we want to see a 400 code to indicate that there was no game time error
        is_server_error = self.screen_mixin(
            screen_name="ImageLocation.LOGIN_SCREEN",
            image_to_compare="server_maintenance_lable",
            skip_sleep=True,
        )
        return is_server_error.request.status_code

    def _validate_password(self):
        # this one is tricky, we want to see a 400 code to indicate that there was no game time error
        is_password_error = self.screen_mixin(
            screen_name="ImageLocation.LOGIN_SCREEN",
            image_to_compare="password_error_lable",
            skip_sleep=True,
        )
        return is_password_error.request.status_code

    def validate_errors(self):
        """Run both validation functions concurrently and handle the results."""

        results = [None, None, None, None, None]

        def validate_internal_error():
            results[0] = self._validate_internal_error()

        def validate_gametime():
            results[1] = self._validate_gametime()

        def validate_email():
            results[2] = self._validate_email()

        def validate_server():
            results[3] = self._validate_server()

        def validate_password():
            results[4] = self._validate_password()

        # Create two threads for the two validation functions
        thread1 = threading.Thread(target=validate_internal_error)
        thread2 = threading.Thread(target=validate_gametime)
        thread3 = threading.Thread(target=validate_email)
        thread4 = threading.Thread(target=validate_server)
        thread5 = threading.Thread(target=validate_password)

        # Start both threads
        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()
        thread5.start()

        # Wait for both threads to finish
        thread1.join()
        thread2.join()
        thread3.join()
        thread4.join()
        thread5.join()

        # Now both tasks are complete, we can act on the results
        (
            internal_error_result,
            gametime_error_result,
            is_email_error,
            is_server_error,
            is_password_error,
        ) = results

        # Perform some action based on the results
        if internal_error_result == 200:
            # login creds were not correct and need to try again
            pass
        if gametime_error_result == 200:
            # character has no valid game time
            pass
        if is_email_error == 200:
            pass
        if is_server_error == 200:
            pass
        if is_password_error == 200:
            pass

        if internal_error_result == 400:
            # everything was input correctly
            pass
        if gametime_error_result == 400:
            # character has game time
            pass
        if is_email_error == 400:
            pass
        if is_server_error == 400:
            pass
        if is_password_error == 400:
            pass

        if internal_error_result and internal_error_result == 400:
            print("Internal error detected!")
        if gametime_error_result and gametime_error_result == 200:
            print("No game time available!")

        # You can return the results or handle them here
        return (
            internal_error_result,
            gametime_error_result,
            is_email_error,
            is_server_error,
            is_password_error,
        )

    def _validate_loading(self):
        is_loading_complete = self.screen_mixin(
            screen_name="ImageLocation.IN_GAME_SCREEN",
            image_to_compare="loading_complete",
            minSearchTime=120,
        )
        return is_loading_complete

    def login(self, character):
        self.character = character

        # self._clear_input_login_fields()
        # self._is_email_field_empty()
        # self._is_password_field_empty()

        # Inside your class
        (
            internal_error_result,
            gametime_error_result,
            is_email_error,
            is_server_error,
            is_password_error,
        ) = self.validate_errors()

        # Handle results further if needed
        if internal_error_result == 400:
            print("Handle the internal error")
        if gametime_error_result == 200:
            print("Handle the gametime issue")

        is_internal_error = self._validate_internal_error()
        if is_internal_error.request.status_code == 400:
            pass

        is_gametime_error = self._validate_gametime()
        # checking if character has NO gametime
        if is_gametime_error.request.status_code == 200:
            logger.debug(f"No game time: {self.character.username}")
            CharacterQuerySet.update_character(
                self.character, {"has_gametime": False, "active": False}
            )
            return

        is_loading_complete = self._validate_loading()
        # checking if character loaded in game within minSearchTime
        if not is_loading_complete.request.status_code == 200:
            logger.warning("Loading in game failed")
            raise

        logger.success(f"{self.character.username} Successfully loaded game")
        CharacterQuerySet.update_character(self.character, {"has_gametime": True})
        self.survey()
        self.welcome_reward()
        return True

    def logout(self, respawn=False):
        loading_complete_response = VerifyScreenMixin(
            screen_name="ImageLocation.IN_GAME_SCREEN",
            image_to_compare="loading_complete",
            skip_sleep=True,
        )
        if loading_complete_response.request.status_code == 400:
            return

        count = 0
        max_count = 20
        at_esc_menu = False
        while not at_esc_menu:
            if count >= max_count:
                break

            # pydirectinput.press("esc")
            # sleep(random.uniform(0.5, 2.0))
            logout_btn_response = VerifyScreenMixin(
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

        logger.error({"success": False, "message": "ESC Menu Not Found"})
        raise Exception("ESC Menu Not Found")

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
        survey = VerifyScreenMixin(
            screen_name="ImageLocation.IN_GAME_SCREEN",
            image_to_compare="survey",
            skip_sleep=True,
        )
        if survey.request.status_code == 200:
            VerifyScreenMixin(
                screen_name="ImageLocation.IN_GAME_SCREEN",
                image_to_compare="survey_skip_btn",
                mouse_click=True,
            )
        return

    @timing_decorator
    def welcome_reward(self):
        """Checks for Daily reward"""
        welcome_screen = VerifyScreenMixin(
            screen_name="ImageLocation.IN_GAME_SCREEN",
            image_to_compare="quanta_lable",
            skip_sleep=True,
        )
        if welcome_screen.request.status_code == 200:
            VerifyScreenMixin(
                screen_name="ImageLocation.IN_GAME_SCREEN",
                image_to_compare="selected_ok_btn",
                mouse_click=True,
            )
        return


if __name__ == "__main__":
    pass

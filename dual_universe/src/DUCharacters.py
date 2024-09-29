import pyautogui

from dual_universe.config.config_manager import timing_decorator
from dual_universe.config.db_setup import EncryptPassword
from dual_universe.integrations.key_board import keyboard_press, keyboard_write
from dual_universe.logs.logging_config import logger
from dual_universe.src.models.image_model import ImageLocation
from dual_universe.src.querysets.character_queryset import CharacterQuerySet
from dual_universe.src.verify_screen import VerifyScreenMixin


class DUCharacters(VerifyScreenMixin):
    def __init__(self):
        pass

    @timing_decorator
    def login(self, character):
        response_du_login_screen_label = VerifyScreenMixin(
            screen_name=ImageLocation.LOGIN_SCREEN,
            image_to_compare="du_login_screen_label",
        )
        # if not at login screen, logout
        if response_du_login_screen_label.request.status_code == 400:
            self.logout()
            return

        attempts = 4
        count = 0
        while count <= attempts:
            logger.info(f"logging into {character.username}")
            keyboard_press("tab")
            keyboard_press("backspace")
            keyboard_press("tab")
            keyboard_press("backspace")

            is_email_field_empty = VerifyScreenMixin(
                screen_name=ImageLocation.LOGIN_SCREEN,
                image_to_compare="email_login",
                mouse_click=True,
                mouse_clicks=4,
            )
            # checking if email field is empty
            if is_email_field_empty.request.status_code == 400:
                count += 1
                continue

            keyboard_write(character.email)
            keyboard_press("tab")

            is_password_field_empty = VerifyScreenMixin(
                screen_name=ImageLocation.LOGIN_SCREEN,
                image_to_compare="password_login",
                mouse_click=True,
                mouse_clicks=4,
                skip_sleep=True,
            )
            # checking if password field is empty
            if is_password_field_empty.request.status_code == 400:
                count += 1
                continue
            decrypt = EncryptPassword()
            keyboard_write(decrypt.decrypt_password(character.password))
            keyboard_press("enter")

            is_internal_error = VerifyScreenMixin(
                screen_name=ImageLocation.LOGIN_SCREEN,
                image_to_compare="internal_error",
                confidence=0.8,
                skip_sleep=True,
            )
            # checking if there is an internal error (incorrect email or password)
            if is_internal_error.request.status_code == 400:
                count += 1
                continue

            is_gametime_error = VerifyScreenMixin(
                screen_name=ImageLocation.LOGIN_SCREEN,
                image_to_compare="gametime_error_lable",
                skip_sleep=True,
            )
            # checking if character has NO gametime
            if is_gametime_error.request.status_code == 200:
                logger.debug(f"No game time: {character.username}")
                CharacterQuerySet.update_character(
                    character, {"has_gametime": False, "active": False}
                )
                return False

            is_loading_complete = VerifyScreenMixin(
                screen_name=ImageLocation.IN_GAME_SCREEN,
                image_to_compare="loading_complete",
                minSearchTime=120,
            )
            # checking if character loaded in game within minSearchTime
            if not is_loading_complete.request.status_code == 200:
                logger.warning("Loading in game failed")
                raise

            logger.success(f"{character.username} Successfully loaded game")
            CharacterQuerySet.update_character(character, {"has_gametime": True})
            self.survey()
            self.welcome_reward()
            return True

    @timing_decorator
    def logout(self, respawn=False):

        loading_complete_response = VerifyScreenMixin(
            screen_name=ImageLocation.IN_GAME_SCREEN,
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
                screen_name=ImageLocation.LOGOUT_SCREEN,
                image_to_compare="logout_btn",
                skip_sleep=True,
                esc=True,
                mouse_click=True,
                mouse_clicks=1,
            )
            if not logout_btn_response.request.status_code == 200:
                count += 1
                continue
            elif logout_btn_response.request.status_code == 200 and respawn:
                return
            at_esc_menu = True
            # pyautogui.click(logout_btn_response['screen_coords'])
            return

        logger.error({"success": False, "message": "ESC Menu Not Found"})
        raise Exception("ESC Menu Not Found")

    def check_location(self):  # TODO: Implement
        """Comes in after welcome back reward"""
        step_scroll = 1000
        # Press F4(map)
        keyboard_press("f4")
        # wait for map loading
        my_marker = VerifyScreenMixin(
            screen_name=ImageLocation.MAP_SCREEN,
            image_to_compare="my_map_marker",
            confidence=0.8,
        )
        # scroll-in(zoom)
        pyautogui.scroll(step_scroll, my_marker)
        # find planet info
        planet_label = VerifyScreenMixin(
            screen_name=ImageLocation.MAP_SCREEN,
            image_to_compare="map_planet_label",
            confidence=0.8,
        )
        # find Market icon
        market_icon = VerifyScreenMixin(
            screen_name=ImageLocation.MAP_SCREEN,
            image_to_compare="map_market_icon",
            confidence=0.8,
        )
        # VerifyScreen Market location
        market_label = VerifyScreenMixin(
            screen_name=ImageLocation.MAP_SCREEN,
            image_to_compare="map_market_label",
            confidence=0.8,
        )
        # close map (Esc)
        keyboard_press("esc")

    @timing_decorator
    def survey(self):
        survey = VerifyScreenMixin(
            screen_name=ImageLocation.IN_GAME_SCREEN,
            image_to_compare="survey",
            skip_sleep=True,
        )
        if survey.request.status_code == 200:
            VerifyScreenMixin(
                screen_name=ImageLocation.IN_GAME_SCREEN,
                image_to_compare="survey_skip_btn",
                mouse_click=True,
            )
        return

    @timing_decorator
    def welcome_reward(self):
        """Checks for Daily reward"""
        welcome_screen = VerifyScreenMixin(
            screen_name=ImageLocation.IN_GAME_SCREEN,
            image_to_compare="quanta_lable",
            skip_sleep=True,
        )
        if welcome_screen.request.status_code == 200:
            VerifyScreenMixin(
                screen_name=ImageLocation.IN_GAME_SCREEN,
                image_to_compare="selected_ok_btn",
                mouse_click=True,
            )
        return


if __name__ == "__main__":
    obj = DUCharacters()
    # obj.login(
    #     character={
    #         "barron",
    #     }
    # )
    obj.logout(respawn=False)

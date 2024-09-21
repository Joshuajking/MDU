import random
from time import sleep

import keyboard
import pyautogui
import pydirectinput

from dual_universe.config.config_manager import timing_decorator
from dual_universe.logs.logging_config import logger
from models.image_model import ImageLocation
from querysets.character_queryset import CharacterQuerySet
from dual_universe.src.verify_screen import VerifyScreenMixin


class DUCharacters(VerifyScreenMixin):
    def __init__(self):
        # self.verify = VerifyScreenMixin()
        pass

    @timing_decorator
    def login(self, character):
        response_du_login_screen_label = True
        while response_du_login_screen_label:
            response_du_login_screen_label = VerifyScreenMixin(
                screen_name=ImageLocation.LOGIN_SCREEN,
                image_to_compare="du_login_screen_label",
                skip_sleep=True,
            )
            if response_du_login_screen_label.request.data["success"]:
                break
            self.logout()

        attempts = 3
        count = 0
        while count <= attempts:
            logger.info(f"logging into {character.username}")

            keyboard.press("tab")
            sleep(0.75)
            keyboard.press("backspace")
            sleep(0.75)
            keyboard.press("tab")
            sleep(0.75)
            keyboard.press("backspace")

            response_email_login = VerifyScreenMixin(
                screen_name=ImageLocation.LOGIN_SCREEN,
                image_to_compare="email_login",
                mouse_click=True,
                mouse_clicks=4,
            )

            sleep(0.75)
            keyboard.write(character.email)
            sleep(0.75)
            pydirectinput.press("tab")

            response_password_login = VerifyScreenMixin(
                screen_name=ImageLocation.LOGIN_SCREEN,
                image_to_compare="password_login",
                mouse_click=True,
                mouse_clicks=4,
            )

            keyboard.write(character.password)
            sleep(random.uniform(0.1, 0.4))
            pydirectinput.press("enter")

            internal_error = VerifyScreenMixin(
                screen_name=ImageLocation.LOGIN_SCREEN,
                image_to_compare="internal_error",
                confidence=0.8,
                minSearchTime=3,
                skip_sleep=True,
            )
            response_email_login = VerifyScreenMixin(
                screen_name=ImageLocation.LOGIN_SCREEN,
                image_to_compare="email_login",
                mouse_click=True,
                minSearchTime=3,
                skip_sleep=True,
            )

            if (
                internal_error.request.data["success"]
                and not response_email_login.request.data["success"]
            ):
                logger.warning({"success": False, "status": "email_field: failed"})
                continue

            response_gametime_error_lable = VerifyScreenMixin(
                screen_name=ImageLocation.LOGIN_SCREEN,
                image_to_compare="gametime_error_lable",
                skip_sleep=True,
            )

            if response_gametime_error_lable.request.data["success"]:
                logger.debug(f"No game time: {character.username}")
                CharacterQuerySet.update_character(
                    character, {"has_gametime": False, "active": False}
                )

                return False

            response_loading_complete = VerifyScreenMixin(
                screen_name=ImageLocation.IN_GAME_SCREEN,
                image_to_compare="loading_complete",
            )

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
        if not loading_complete_response.request.data["success"]:
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
            if not logout_btn_response["success"]:
                count += 1
                continue
            elif logout_btn_response["success"] and respawn:
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
        pydirectinput.press("f4")
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
        pydirectinput.press("esc")

    @timing_decorator
    def survey(self):
        survey = VerifyScreenMixin(
            screen_name=ImageLocation.IN_GAME_SCREEN,
            image_to_compare="survey",
            skip_sleep=True,
        )
        if survey["screen_coords"] is not None:
            VerifyScreenMixin(
                screen_name=ImageLocation.IN_GAME_SCREEN,
                image_to_compare="survey_skip_btn",
                skip_sleep=True,
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
        if welcome_screen["screen_coords"] is not None:
            VerifyScreenMixin(
                screen_name=ImageLocation.IN_GAME_SCREEN,
                image_to_compare="selected_ok_btn",
                skip_sleep=True,
                mouse_click=True,
            )
        return


if __name__ == "__main__":
    obj = DUCharacters()
    obj.login(
        character={
            "barron",
        }
    )
    obj.logout(respawn=False)

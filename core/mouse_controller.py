import random

import pyautogui
import pydirectinput
import pytweening
from loguru import logger


class MouseControllerMixin:
    @staticmethod
    def simulate_mouse(dest_x, dest_y, mouse_click=False, mouse_clicks=0):
        if mouse_click is True and mouse_clicks == 0:
            logger.debug(
                f"Did you mean to have mouse_clicks = 0: defaulting to mouse_clicks = 1"
            )
            mouse_clicks = 1
        EASING_FUNCTIONS = {
            # "linear": pytweening.linear,
            "easeInQuad": pytweening.easeInQuad,
            "easeOutQuad": pytweening.easeOutQuad,
            "easeInOutQuad": pytweening.easeInOutQuad,
            "easeInCubic": pytweening.easeInCubic,
            "easeOutCubic": pytweening.easeOutCubic,
            "easeInOutCubic": pytweening.easeInOutCubic,
            "easeInQuart": pytweening.easeInQuart,
            "easeOutQuart": pytweening.easeOutQuart,
            "easeInOutQuart": pytweening.easeInOutQuart,
            "easeInQuint": pytweening.easeInQuint,
            "easeOutQuint": pytweening.easeOutQuint,
            "easeInOutQuint": pytweening.easeInOutQuint,
            "easeInSine": pytweening.easeInSine,
            "easeOutSine": pytweening.easeOutSine,
            "easeInOutSine": pytweening.easeInOutSine,
            "easeInExpo": pytweening.easeInExpo,
            "easeOutExpo": pytweening.easeOutExpo,
            "easeInOutExpo": pytweening.easeInOutExpo,
            "easeInCirc": pytweening.easeInCirc,
            "easeOutCirc": pytweening.easeOutCirc,
            "easeInOutCirc": pytweening.easeInOutCirc,
        }

        # Generate a random key
        easing_key = random.choice(list(EASING_FUNCTIONS.keys()))

        # Get the selected easing function object
        selected_easing_function = EASING_FUNCTIONS[easing_key]

        x = random.randint(-23, 27)
        x += dest_x

        y = random.randint(-32, 44)
        y += dest_y

        pyautogui.moveTo(
            x,
            y,
            duration=random.uniform(0.1, 2.2),
            tween=selected_easing_function,
            _pause=True,
        )

        # Use the selected easing function in pyautogui.moveTo
        pyautogui.moveTo(
            dest_x,
            dest_y,
            duration=random.uniform(0.1, 1.2),
            tween=selected_easing_function,
            _pause=True,
        )
        if mouse_click:
            # pyautogui.click(clicks=mouse_clicks, duration=random.uniform(0.2, 0.4))
            pydirectinput.click(clicks=mouse_clicks, interval=0.2)

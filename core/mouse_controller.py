import abc
import random

import pyautogui
import pydirectinput
import pytweening
from loguru import logger


class MouseControllerMixin:
    def __init__(self, dest_x, dest_y, mouse_click=False, mouse_clicks=0):
        self.dest_x = dest_x
        self.dest_y = dest_y
        self.mouse_click = mouse_click
        self.mouse_clicks = mouse_clicks
        if self.mouse_click is True and self.mouse_clicks == 0:
            logger.debug(
                f"Did you mean to have mouse_clicks = 0: defaulting to mouse_clicks = 1"
            )
            self.mouse_clicks = 1

    def simulate_mouse(self):
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
        x += self.dest_x

        y = random.randint(-32, 44)
        y += self.dest_y

        pyautogui.moveTo(
            x,
            y,
            duration=random.uniform(0.1, 2.2),
            tween=selected_easing_function,
            _pause=True,
        )

        # Use the selected easing function in pyautogui.moveTo
        pyautogui.moveTo(
            self.dest_x,
            self.dest_y,
            duration=random.uniform(0.1, 1.2),
            tween=selected_easing_function,
            _pause=True,
        )
        if self.mouse_click:
            # pyautogui.click(clicks=mouse_clicks, duration=random.uniform(0.2, 0.4))
            pydirectinput.click(clicks=self.mouse_clicks, interval=0.2)
        return

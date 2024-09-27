from time import sleep

import keyboard
import pydirectinput
import pyautogui


def pydirectinput_press(*args, **kwargs):
    pydirectinput.press(*args)
    sleep(kwargs.get("sleep", 0))


def keyboard_press(*args, **kwargs):
    keyboard.press(*args)
    sleep(kwargs.get("sleep", 0.75))


def keyboard_write(*args, **kwargs):
    keyboard.write(*args)
    sleep(kwargs.get("sleep", 0.75))


if __name__ == "__main__":
    keyboard_press("tab")

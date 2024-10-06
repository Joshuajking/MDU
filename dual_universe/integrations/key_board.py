from time import sleep

import keyboard


def keyboard_press(*args, **kwargs):
    keyboard.press(*args)
    sleep(kwargs.get("sleep", 0.75))


def keyboard_write(*args, **kwargs):
    keyboard.write(*args)
    sleep(kwargs.get("sleep", 0.75))

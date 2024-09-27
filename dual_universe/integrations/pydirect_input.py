from time import sleep

import pydirectinput


def pydirectinput_press(*args, **kwargs):
    pydirectinput.press(*args)
    sleep(kwargs.get("sleep", 0))
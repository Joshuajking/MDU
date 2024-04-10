# Simulate pressing the Windows key, Alt key, and R key simultaneously
import time

import pydirectinput


def get_last_30_seconds():
	pydirectinput.keyDown('win')
	pydirectinput.keyDown('alt')
	pydirectinput.keyDown('g')

	# Wait for a short delay to ensure the keys are pressed simultaneously
	time.sleep(0.1)

	# Release the keys
	pydirectinput.keyUp('win')
	pydirectinput.keyUp('alt')
	pydirectinput.keyUp('g')

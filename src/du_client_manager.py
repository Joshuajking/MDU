import os
import subprocess
import sys
import time

import psutil
import pynput

from src.config_manager import ConfigManager, timing_decorator
from src.logging_config import logger
from src.models import ImageLocation
from src.verify_screen import VerifyScreen


class DUClientManager:
	def __init__(self):
		self.config_manager = ConfigManager()
		self.verify = VerifyScreen()
		self.game_client = self.config_manager.get_value('config.game_client')
		self.app_path = self.config_manager.get_value('config.app_path')
		self.DEBUG_MODE = self.is_debugging()
		self.mouse_listener = pynput.mouse.Listener(suppress=True)
		self.keyboard_listener = pynput.keyboard.Listener(suppress=True)

	@staticmethod
	def is_debugging():
		"""Check if the code is running in a debugger."""
		return os.environ.get("DEBUG_MODE", "0") == "1"

	def is_client_running(self) -> int | None:
		"""Check if the game_client is running."""
		pid = None
		list_of_processes = []

		# if sys.platform not in ('java', 'darwin', 'win32'):  # todo: build this out
		if not sys.platform == 'win32':
			raise NotImplementedError()

		if self.is_debugging():
			self.mouse_listener.start()
			self.keyboard_listener.start()
			logger.debug("Debug mode is active. Some code is disabled.")

		for process in psutil.process_iter(['pid', 'name', 'create_time']):
			list_of_processes.append(process)
			if process.info['name'] == self.game_client:
				pid = process.info['pid']
				_start_time = process.info['create_time']
				logger.debug(f'{self.game_client}: {process}, started at {_start_time}')
				break
		if not isinstance(pid, int):
			logger.debug(f'{self.game_client} not running, pid:{pid}')

		if not self.DEBUG_MODE:
			self.mouse_listener.stop()
			self.keyboard_listener.stop()

		return pid

	def geforce_client(self):
		self.verify.screen(
			screen_name=ImageLocation.GEFORCE_SCREEN,
			image_to_compare="geforce_select_game",
			verify_screen=True
		)
		self.verify.screen(
			screen_name=ImageLocation.GEFORCE_SCREEN,
			image_to_compare="geforce_select_game",
			mouse_click=True
		)
		## xxx: this is for NovaQuark GeforceNow version not Steam version
		# self.verify.screen(
		# 	screen_name=ImageLocation.GEFORCE_SCREEN,
		# 	image_to_compare="geforce_play_btn",
		# 	mouse_click=True
		# )

	@timing_decorator
	def start_application(self):
		"""Start the game_client application if not already running."""
		client_pid = self.is_client_running()
		if not isinstance(client_pid, int):
			try:
				# Start the application
				subprocess.Popen(self.app_path)
				logger.debug(f'Started game client: {self.app_path}')
			except Exception as e:
				logger.error(f"Error while starting the application: {e}, {self.app_path}")
			if self.game_client == "GeForceNOW.exe":
				self.geforce_client()
			self.verify.screen(
				screen_name=ImageLocation.LOGIN_SCREEN,
				image_to_compare="du_login_screen_label",
				verify_screen=True
			)
			logger.success(f"game client started: {self.app_path}")
		else:
			logger.debug(f"game client running already")

	def stop_application(self):
		"""Stop the game_client application if running."""
		client_running = True
		while client_running:
			client_pid = self.is_client_running()
			if isinstance(client_pid, int):
				client_running = True
				logger.info("Client is running. Stopping...")
				try:
					process = psutil.Process(client_pid)
					process.terminate()
					process.wait(timeout=5)
					continue
				except psutil.TimeoutExpired:
					process.kill()
					continue
				except Exception as e:
					logger.error(f"Error while stopping the application: {e}")
					raise EnvironmentError(f"Error while stopping the application:")
			client_running = False
			logger.success(f"Client shutdown successfully")


if __name__ == '__main__':
	start_time = time.perf_counter()
	du_client = DUClientManager()
	du_client.start_application()
	du_client.stop_application()
	end_time = time.perf_counter()
	elapsed_time = end_time - start_time
	print(f"Elapsed time: {elapsed_time}")
	pass

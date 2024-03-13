from time import perf_counter, sleep

import pyautogui
from logs.logging_config import logger

from config.config_manager import ConfigManager
from config.db_setup import DbConfig
from core.DUCharacters import DUCharacters
from core.DUClientManager import DUClientManager
from core.DUFlight import DUFlight
from core.DUMissions import DUMissions
from querysets.querysets import CharacterQuerySet
from utils.transfer_money import TransferMoney


class EngineLoop:

	def __init__(self):
		super().__init__()
		DbConfig().load_image_entries_to_db()
		self.config_manager = ConfigManager()
		self.du_characters = DUCharacters()
		self.missions = DUMissions()
		self.flight = DUFlight()
		self.client = DUClientManager()
		self.client.start_application()
		self.transfer = TransferMoney()
		self.pilot = CharacterQuerySet.read_character_by_username(self.config_manager.get_value('config.pilot'))
		self.screen_w, self.screen_h = pyautogui.size()
		self.screen_size = (self.screen_w, self.screen_h)
		self.retrieve_mode = True
		self.package_count = 0
		self.percentage = 0
		self.active_character_count = None
		self.all_active_characters = None
		self.flight_status = None

	def active_package_count(self, ):
		# is_active = CharacterQuerySet.count_active_characters()
		self.package_count = CharacterQuerySet.count_has_package_characters()

		if self.active_character_count > 0:
			self.percentage = (self.package_count / self.active_character_count) * 100
			if self.percentage >= 75:
				self.retrieve_mode = False
			else:
				self.retrieve_mode = True
		else:
			self.percentage = 0

	def engine(self):
		trips = 0
		max_trips = 20

		self.all_active_characters = CharacterQuerySet.get_active_characters()
		self.active_character_count = CharacterQuerySet.count_active_characters()

		while self.active_character_count > 0 and trips < max_trips:
			trip_time_start = perf_counter()
			tt_char_time = 0
			for character in self.all_active_characters:
				character_time_start = perf_counter()
				# Start login
				has_gametime = self.du_characters.login(character)

				if not has_gametime:
					continue
				status = self.missions.process_package()
				logger.info(f"{character.username} package status: {status}")
				CharacterQuerySet.update_character(character, {'has_package': status["has_package"]})

				self.du_characters.logout()
				character_time_stop = perf_counter()
				char_time = character_time_stop - character_time_start
				tt_char_time += char_time
				logger.info(f"retrieve_mode: {self.retrieve_mode}")
				logger.info(f"package_count: {self.package_count}")
				logger.info(f"character elapse: {character_time_stop - character_time_start:.2f} seconds")
				logger.info(f"total character elapse: {tt_char_time/60:.2f} minutes")
				logger.info(f"trips: {trips}/max_trips:{max_trips}")
				continue

			self.active_package_count()
			logger.info(f"retrieve_mode: {self.retrieve_mode}")
			logger.info(f"percentage of package taken: {self.percentage}")

			logger.info(f"Logging into Pilot: {self.pilot.username}")
			self.du_characters.login(self.pilot)
			self.flight.mission_flight(self.retrieve_mode)
			trips += 1
			trip_time_stop = perf_counter()
			tt_trip_time = trip_time_stop - trip_time_start
			logger.info(f"trip elapse: {tt_trip_time/60:.2f} minutes")
			continue


if __name__ == "__main__":
	client_limit = 21600
	client_run = 0
	client_start = perf_counter()
	while True:
		start = EngineLoop()
		try:
			start.engine()
		except Exception as e:
			logger.error(f"Exception: {str(e)}")
			start.client.stop_application()
			DUCharacters().logout()
			sleep(20)
			continue
		start.client.stop_application()
		sleep(20)
		client_stop = perf_counter()
		client_runtime = client_stop - client_start
		client_run += client_runtime
		if client_run >= client_limit:
			break



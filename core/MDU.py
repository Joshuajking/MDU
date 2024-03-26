from time import perf_counter, sleep

import pyautogui

from config.config_manager import ConfigManager
from config.db_setup import DbConfig
from core.DUCharacters import DUCharacters
from core.DUClientManager import DUClientManager
from core.DUFlight import DUFlight
from core.DUMissions import DUMissions
from logs.logging_config import logger
from querysets.querysets import CharacterQuerySet
from utils.transfer_money import TransferMoney


class EngineLoop:

	def __init__(self):
		# super().__init__()
		# DbConfig().load_image_entries_to_db()
		# self.config_manager = ConfigManager()
		# self.du_characters = DUCharacters()
		# self.missions = DUMissions()
		# self.flight = DUFlight()
		# self.client = DUClientManager()
		# self.client.start_application()
		# self.mission_meta = MissionMetaQuerySet()
		# self.pilot = CharacterQuerySet.read_character_by_username(self.config_manager.get_value('config.pilot'))
		# self.screen_w, self.screen_h = pyautogui.size()
		# self.screen_size = (self.screen_w, self.screen_h)
		self.retrieve_mode = True

	# self.active_character_count = None
	# self.all_active_characters = None
	# self.flight_status = None
	# self.package_count = CharacterQuerySet.count_has_package_characters()

	def active_package_count(self):
		package_count = CharacterQuerySet.count_has_package_characters()
		logger.info(f"package_count: {package_count}")
		active_character_count = CharacterQuerySet.count_active_characters()

		if active_character_count > 0:
			percentage = (package_count / active_character_count) * 100
			logger.info(f"percentage of package taken: {percentage}")
			if percentage >= 75:
				self.retrieve_mode = False
			else:
				self.retrieve_mode = True

	def engine(self):
		trips = 0
		max_trips = 5
		du_characters = DUCharacters()
		flight = DUFlight()
		missions = DUMissions()
		round_trips = MissionMetaQuerySet()
		config_manager = ConfigManager()

		all_active_characters = CharacterQuerySet.get_active_characters()
		active_character_count = CharacterQuerySet.count_active_characters()

		while active_character_count > 0 and trips < max_trips:
			trip_time_start = perf_counter()
			tt_char_time = 0
			for character in all_active_characters:
				# if character.has_package and self.retrieve_mode:
				# 	continue
				character_time_start = perf_counter()
				# Start login
				has_gametime = du_characters.login(character)
				if not has_gametime:
					continue
				sleep(3)

				status = missions.process_package(character)

				logger.info(f"{character.username} package status: {status}")
				CharacterQuerySet.update_character(character, {'has_package': status["has_package"]})

				du_characters.logout()
				character_time_stop = perf_counter()
				char_time = character_time_stop - character_time_start
				tt_char_time += char_time

				round_trips.read_round_trips()
				logger.info(f"round trips: {round_trips}")

				logger.info(f"trips: {trips}/max_trips:{max_trips}")
				logger.info(f"total character elapse: {tt_char_time / 60:.2f} minutes")
				logger.info(f"character elapse: {character_time_stop - character_time_start:.2f} seconds")
				logger.info(f"retrieve_mode: {self.retrieve_mode}")
				# logger.info(f"package_count: {self.package_count}")

				continue

			self.active_package_count()
			logger.info(f"retrieve_mode: {self.retrieve_mode}")

			pilot = CharacterQuerySet.read_character_by_username(config_manager.get_value('config.pilot'))
			logger.info(f"Logging into Pilot: {pilot.username}")

			du_characters.login(pilot)

			flight.mission_flight(self.retrieve_mode)

			trips += 1
			trip_time_stop = perf_counter()
			tt_trip_time = trip_time_stop - trip_time_start
			logger.info(f"trip elapse: {tt_trip_time / 60:.2f} minutes")
			continue


if __name__ == "__main__":
	from querysets.querysets import MissionMetaQuerySet

	pre_load = DbConfig()
	pre_load.load_image_entries_to_db()
	client_limit = 21600
	client_run = 0
	bulk_trip = 0
	client_start = perf_counter()
	client = DUClientManager()
	while True:
		start = EngineLoop()
		client.start_application()
		try:
			start.engine()
		except Exception as e:
			logger.error(f"Exception: {str(e)}")
			client.stop_application()
			client_stop = perf_counter()
			client_runtime = client_stop - client_start
			client_run += client_runtime
			logger.info(f"Client runtime: {client_run}")
			sleep(20)
			continue
		else:
			client.stop_application()
			sleep(20)
			MissionMetaQuerySet().create_or_update_round_trips(1)
			logger.info(f"Bulk trips: {bulk_trip}")
			client_stop = perf_counter()
			client_runtime = client_stop - client_start
			client_run += client_runtime
			logger.info(f"Client runtime: {client_run}")
			if client_run >= client_limit:
				break

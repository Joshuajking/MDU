import random
from time import perf_counter, sleep

from config.config_manager import ConfigManager
from config.db_setup import DbConfig
from core.DUCharacters import DUCharacters
from core.DUClientManager import DUClientManager
from core.DUFlight import DUFlight
from core.DUMissions import DUMissions
from logs.logging_config import logger
from querysets.querysets import CharacterQuerySet


class EngineLoop:

	def __init__(self):
		self.retrieve_mode = True

	def active_package_count(self):
		package_count = CharacterQuerySet.count_has_package_and_active_characters()
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
		max_trips = 2

		du_characters = DUCharacters()
		flight = DUFlight()
		missions = DUMissions()
		# round_trips = MissionMetaQuerySet()
		config_manager = ConfigManager()

		all_active_characters = CharacterQuerySet.get_active_characters()
		active_character_count = CharacterQuerySet.count_active_characters()
		self.active_package_count()

		while active_character_count > 0 and trips < max_trips:
			trip_time_start = perf_counter()
			tt_char_time = 0
			for character in all_active_characters:
				if self.retrieve_mode and character.has_package:
					continue
				elif not self.retrieve_mode and not character.has_package:
					continue

				character_time_start = perf_counter()
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

				logger.info(f"Summary"
				            f"trips: {trips}/max_trips:{max_trips} \n"
				            f"total character elapse: {tt_char_time / 60:.2f} minutes \n"
				            f"character elapse: {character_time_stop - character_time_start:.2f} seconds \n"
				            f"retrieve_mode: {self.retrieve_mode} \n")

				continue

			self.active_package_count()

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
	# from querysets.querysets import MissionMetaQuerySet

	pre_load = DbConfig()
	pre_load.load_image_entries_to_db()
	client_limit = 43200
	client_run = 0
	bulk_trip = 0
	client_start = perf_counter()
	client = DUClientManager()
	start = EngineLoop()
	while True:
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
			sleep(random.uniform(10, 30))
			continue
		else:
			sleep(random.uniform(10, 30))
			client.stop_application()
			sleep(random.uniform(10, 30))
			# MissionMetaQuerySet().create_or_update_round_trips(1)
			logger.info(f"Bulk trips: {bulk_trip}")
			client_stop = perf_counter()
			client_runtime = client_stop - client_start
			client_run += client_runtime
			logger.info(f"Client runtime: {client_run}")
			if client_run >= client_limit:
				break

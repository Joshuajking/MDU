# from time import perf_counter, sleep
#
# import pyautogui
#
# from config.config_manager import ConfigManager
# from config.db_setup import DbConfig
# from core.DUCharacters import DUCharacters
# from core.DUClientManager import DUClientManager
# from core.DUFlight import DUFlight
# from core.DUMissions import DUMissions
# from logs.logging_config import logger
# from querysets.querysets import CharacterQuerySet, MissionMetaQuerySet
# from utils.transfer_money import TransferMoney
#
#
# class EngineLoop:
#
# 	def __init__(self, running_event):
# 		self.retrieve_mode = True
# 		self._running = running_event
#
# 	def active_package_count(self):
# 		package_count = CharacterQuerySet.count_has_package_characters()
# 		logger.info(f"package_count: {package_count}")
# 		active_character_count = CharacterQuerySet.count_active_characters()
#
# 		if active_character_count > 0:
# 			percentage = (package_count / active_character_count) * 100
# 			logger.info(f"percentage of package taken: {percentage}")
# 			if percentage >= 75:
# 				self.retrieve_mode = False
# 			else:
# 				self.retrieve_mode = True
#
# 	def engine(self):
# 		du_characters = DUCharacters()
# 		flight = DUFlight()
# 		missions = DUMissions()
# 		config_manager = ConfigManager()
#
# 		all_active_characters = CharacterQuerySet.get_active_characters()
# 		active_character_count = CharacterQuerySet.count_active_characters()
#
# 		while self._running.is_set() and active_character_count > 0:
# 			for character in all_active_characters:
# 				# Check if the _running event is cleared
# 				if not self._running.is_set():
# 					break
# 				# if character.has_package and self.retrieve_mode:
# 				# 	continue
# 				character_time_start = perf_counter()
# 				# Start login
# 				has_gametime = du_characters.login(character)
# 				if not has_gametime:
# 					continue
# 				sleep(3)
#
# 				status = missions.process_package(character)
#
# 				logger.info(f"{character.username} package status: {status}")
# 				CharacterQuerySet.update_character(character, {'has_package': status["has_package"]})
#
# 				du_characters.logout()
# 				logger.info(f"retrieve_mode: {self.retrieve_mode}")
# 				continue
#
# 			self.active_package_count()
# 			logger.info(f"retrieve_mode: {self.retrieve_mode}")
#
# 			pilot = CharacterQuerySet.read_character_by_username(config_manager.get_value('config.pilot'))
# 			logger.info(f"Logging into Pilot: {pilot.username}")
# 			du_characters.login(pilot)
# 			flight.mission_flight(self.retrieve_mode)
# 			continue
#
#
# if __name__ == "__main__":
# 	pre_load = DbConfig()
# 	pre_load.load_image_entries_to_db()
# 	client_limit = 21600
# 	client_run = 0
# 	bulk_trip = 0
# 	client_start = perf_counter()
# 	client = DUClientManager()
# 	start = EngineLoop()
# 	while True:
# 		client.start_application()
# 		try:
# 			start.engine()
# 		except Exception as e:
# 			logger.error(f"Exception: {str(e)}")
# 			client.stop_application()
# 			client_stop = perf_counter()
# 			client_runtime = client_stop - client_start
# 			client_run += client_runtime
# 			logger.info(f"Client runtime: {client_run}")
# 			sleep(20)
# 			continue
# 		else:
# 			client.stop_application()
# 			sleep(20)
# 			MissionMetaQuerySet().create_or_update_round_trips(1)
# 			logger.info(f"Bulk trips: {bulk_trip}")
# 			client_stop = perf_counter()
# 			client_runtime = client_stop - client_start
# 			client_run += client_runtime
# 			logger.info(f"Client runtime: {client_run}")
# 			if client_run >= client_limit:
# 				break

import unittest
from unittest.mock import MagicMock

from core import MDU
from core.MDU import EngineLoop


class TestMDU(unittest.TestCase):
	def setUp(self) -> None:
		pass

	def tearDown(self) -> None:
		pass

	def test_active_package_count_1_character_1_package(self, mock_package_count, mock_active_character_count):
		mock_package_count.return_value = 1
		mock_active_character_count.return_value = 1
		# EngineLoop = MagicMock()
		class_instance = EngineLoop()

		result = class_instance.active_package_count()


import unittest
from unittest import mock
from unittest.mock import patch, MagicMock

from sqlmodel import create_engine, SQLModel
from utils.verify_screen import VerifyScreen
from utils.special_mission_ocr import OCREngine
from core.DUMissions import DUMissions
import utils.verify_screen
from querysets import querysets
import time

from utils.special_mission_ocr import ResponseData


class TestProcessPackage(unittest.TestCase):
    def setUp(self):
        self.character = MagicMock()
        self.missions = DUMissions()
        self.mock_verify_screen = MagicMock()
        self.missions.verify.screen = self.mock_verify_screen

    def test_process_package_deliver_success(self):
        self.mock_verify_screen.return_value = {'success': True}
        result = self.missions.process_package(self.character, is_retrieve=False)
        self.assertEqual(result, {'has_package': False})

    def test_process_package_retrieve_success(self):
        self.mock_verify_screen.return_value = {'success': True}
        result = self.missions.process_package(self.character, is_retrieve=False)
        self.assertEqual(result, {'has_package': True})

    def test_process_package_no_action(self):
        result = self.missions.process_package(self.character, is_retrieve=None)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()

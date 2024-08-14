import os
import unittest
from unittest.mock import patch, MagicMock

from src.config_manager import ConfigManagerMixin
from src.du_client_manager import DUClientManager
from src.verify_screen import VerifyScreen


class TestDUClientManager(unittest.TestCase):

    def setUp(self):
        self.config_manager = ConfigManagerMixin()
        self.client_manager = DUClientManager()
        self.verify = VerifyScreen()
        self.game_client = self.config_manager.get_value("config.game_client")

    def test_debug_mode_enabled(self):
        os.environ["DEBUG_MODE"] = "1"
        self.assertTrue(self.client_manager.is_debugging())
        del os.environ["DEBUG_MODE"]

    def test_debug_mode_disabled(self):
        os.environ["DEBUG_MODE"] = "0"
        self.assertFalse(self.client_manager.is_debugging())
        del os.environ["DEBUG_MODE"]

    def test_debug_mode_default(self):
        self.assertFalse(self.client_manager.is_debugging())

    @patch("src.du_client_manager.psutil.process_iter")
    def test_is_client_running_client_running(self, mock_process_iter):
        mock_process = MagicMock()
        mock_process.info = {
            "name": self.game_client,
            "pid": 12345,
            "create_time": 1234567890,
        }
        mock_process_iter.return_value = [mock_process]
        pid = self.client_manager.is_client_running()
        self.assertEqual(pid, 12345)

    @patch("src.du_client_manager.psutil.process_iter")
    def test_is_client_running_client_not_running(self, mock_process_iter):
        mock_process_iter.return_value = []  # Simulate no processes running
        pid = self.client_manager.is_client_running()
        self.assertIsNone(pid)

    # @patch('src.verify_screen.VerifyScreen.screen')
    # def test_geforce_client_running(self, mock_verify_screen):  # fixme
    # 	mock_instance = mock_verify_screen.return_value
    # 	mock_instance.screen.return_value = (100, 200)  # Return some coordinates
    #
    # 	result = self.client_manager.geforce_client()
    # 	self.assertEqual(result, (100, 200))

    def test_geforce_client_not_running(self):
        pass


if __name__ == "__main__":
    unittest.main()

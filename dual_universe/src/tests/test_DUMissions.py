import unittest
from unittest.mock import patch, Mock

from models.models import SearchAreaLocation


class TestProcessPackage(unittest.TestCase):
    def setUp(self):
        self.character = Mock()
        self.du_missions = Mock()

    def test_retrieve_package(self):
        # Patch the functions with specific return values
        with patch(
            "utils.special_mission_ocr.OCREngine.ocr_missions"
        ) as mock_ocr_missions, patch(
            "utils.verify_screen.VerifyScreen.screen"
        ) as mock_screen, patch(
            "core.DUMissions.ocr.OCREngine.ocr_missions"
        ) as mock_active_taken_missions:
            # Set the return value for each function
            mock_ocr_missions.return_value = {
                "success": True,
                "message": "TEXT_FOUND",
                "TEXT": "Correct Text",
            }
            mock_screen.return_value = {
                "success": True,
                "screen_coords": "screen_coords=True",
            }

            result_setup_mission = self.du_missions.setup_mission()
            result_ocr = self.du_missions.ocr.ocr_missions(
                search_area=SearchAreaLocation.ACTIVE_TAKEN_MISSIONS,
                search_text="test_mission",
                click=True,
            )
            # result_process_package = self.du_missions.process_package(self.character, is_retrieve=True)

            # Assert that the result is correct based on the specified arguments
            # Add your assertions here based on the expected result
            self.assertEqual(result_ocr, {"is_active_mission.success": True})
            # self.assertIsNone()
            # self.assertEqual(result_setup_mission, {"has_package": True})


if __name__ == "__main__":
    unittest.main()

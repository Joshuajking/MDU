import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

from dual_universe.src.DUCharacters import DUCharacters
from dual_universe.util.response import Response


class TestDUCharacters(unittest.TestCase):
    def setUp(self):
        # Set up a mock user
        self.user = MagicMock()
        self.user.username = "barron"
        self.user.email = "barron@example.com"
        self.user.password = "encrypted_password"

    @patch("dual_universe.src.verify_screen.pyautogui.locateOnScreen")
    @patch(
        "dual_universe.src.querysets.image_queryset.ImageQuerySet.read_image_by_name"
    )
    @patch("dual_universe.src.verify_screen.VerifyScreenMixin.screen")
    @patch("dual_universe.src.models.image_model.ImageLocation")
    @patch("dual_universe.integrations.key_board.keyboard_press")
    @patch("dual_universe.integrations.key_board.keyboard_write")
    def test_login_field_input_and_validation(
        self,
        mock_keyboard_write,
        mock_keyboard_press,
        mock_ImageLocation,
        mock_screen,
        mock_read_image,
        mock_locate_on_screen,
    ):
        # Mock the image data returned by ImageQuerySet
        mock_read_image.return_value = MagicMock(image_url="test_image_path")

        # Simulate the behavior of pyautogui.locateOnScreen
        mock_locate_on_screen.side_effect = [
            None,  # Simulate failure for the login screen
            (10, 10, 100, 100),  # Simulate success for email field
            (10, 10, 100, 100),  # Simulate success for password field
        ]

        # Mock the responses for screen verification
        mock_screen.side_effect = [
            Response(
                status_code=400, response_data={"success": False}
            ),  # Login screen not found
            Response(
                status_code=200, response_data={"success": True}
            ),  # Email field found
            Response(
                status_code=200, response_data={"success": True}
            ),  # Password field found
        ]

        mock_ImageLocation.LOGIN_SCREEN = "login_screen"

        # Create an instance of DUCharacters
        obj = DUCharacters()

        # Call the method
        obj.login_field_input_and_validation(self.user)

        # Assert that the locateOnScreen was called with the correct image path
        mock_locate_on_screen.assert_any_call(
            str(Path("test_image_path").resolve()), confidence=0.8
        )

        # Assert that the email and password fields were written correctly
        mock_keyboard_write.assert_any_call(self.user.email)
        mock_keyboard_press.assert_any_call("tab")

        # Verify that the correct responses are returned for each screen
        self.assertEqual(
            mock_screen.call_count, 3
        )  # Login screen, email, and password checks

        # Check if keyboard actions were called correctly for email and password
        mock_keyboard_press.assert_any_call("enter")

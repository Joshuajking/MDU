import unittest
from unittest.mock import patch, MagicMock

from dual_universe.src.verify_screen import VerifyScreenMixin


class TestVerifyScreenMixin(unittest.TestCase):
    @patch(
        "dual_universe.src.querysets.image_queryset.ImageQuerySet.read_image_by_name"
    )
    @patch("pyautogui.locateOnScreen")
    @patch("pydirectinput.press")
    @patch("pyautogui.moveTo")
    def test_screen_image_found(
        self, mock_move_to, mock_press, mock_locate_on_screen, mock_read_image_by_name
    ):
        # Arrange
        mock_read_image_by_name.return_value = MagicMock(
            image_url="fake_image_url", region=(0, 0, 100, 100), image_location="test1"
        )
        mock_locate_on_screen.return_value = (10, 20, 30, 40)

        # Create an instance of VerifyScreenMixin
        screen = VerifyScreenMixin(
            screen_name="testone",
            image_to_compare="testone",
            skip_sleep=True,
            mouse_click=True,
            esc=True,
        )

        # Assert
        self.assertTrue(screen.request.status_code == 200)
        self.assertEqual(screen.request.data["screen_coords"], (25, 40))
        # mock_press.assert_called_with("esc")
        # mock_move_to.assert_called()  # Ensure moveTo was called

    @patch(
        "dual_universe.src.querysets.image_queryset.ImageQuerySet.read_image_by_name"
    )
    @patch("pyautogui.locateOnScreen")
    def test_screen_image_not_found(
        self, mock_locate_on_screen, mock_read_image_by_name
    ):
        # Arrange
        mock_read_image_by_name.return_value = MagicMock(
            image_url="fake_image_url", region=(0, 0, 100, 100), image_location="test1"
        )
        mock_locate_on_screen.return_value = None  # Simulate image not found

        # Create an instance of VerifyScreenMixin
        screen = VerifyScreenMixin(screen_name="test1", image_to_compare="testone")

        # Assert
        self.assertEqual(screen.request.status_code, 400)
        self.assertIsNone(screen.request.data["screen_coords"])


if __name__ == "__main__":
    unittest.main()

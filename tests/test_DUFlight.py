import unittest
from unittest.mock import patch, MagicMock

from MDU.src.du_flight import DUFlight


class TestCheckImgToLand(unittest.TestCase):

    @patch('time.sleep', MagicMock())  # Mock time.sleep to avoid actual waiting
    @patch('pyautogui.locateCenterOnScreen')
    def test_check_img_to_land(self, mock_locate_center):
        # Set up the mock to return screen coordinates after a certain number of calls
        mock_locate_center.return_value = (100, 100)

        # Create an instance of YourClass
        class_instance = DUFlight()

        # Call the method under test
        result = class_instance.check_img_to_land()

        # Assert that the method returns None when image is found
        # self.assertIsNone(result)

        # Assert that the method breaks out of the loop when image is found
        self.assertEqual(mock_locate_center.call_count, 2)


if __name__ == '__main__':
    unittest.main()

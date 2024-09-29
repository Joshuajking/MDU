import random
import time
from dataclasses import dataclass
from pathlib import Path
from time import sleep
from typing import Optional

import pyautogui
import pydirectinput

from dual_universe.logs.logging_config import logger
from dual_universe.src.models.image_model import ImageLocation
from dual_universe.src.mouse_controller import MouseControllerMixin
from dual_universe.util.response import Response
from dual_universe.src.querysets.image_queryset import ImageQuerySet

# Define a base directory for all images
# base_image_dir = Path(__file__).parent.parent / "data" / "images"
base_image_dir = Path(__file__).parent.parent


class ImageNotFound(Exception):
    # Define a custom exception class
    def __init__(self, message=None, error_code=None):
        super().__init__(message)  # Initialize the base Exception class
        self.error_code = error_code  # Custom attribute for additional info

    def __str__(self):
        # Customize the string representation of the exception
        if self.error_code is not None:
            return f"{super().__str__()} (Error Code: {self.error_code})"
        return super().__str__()


@dataclass
class VerifyScreenMixin(MouseControllerMixin):
    screen_name: Optional[ImageLocation | str]
    image_to_compare: str
    confidence: float = 0.8
    minSearchTime: float = 60
    mouse_clicks: int = 0
    skip_sleep: bool = False
    mouse_click: bool = False
    # region: Union[tuple, int] = None
    esc: bool = False
    check_count = 0
    max_checks = 60

    def __post_init__(self):
        if self.skip_sleep:
            self.minSearchTime = 3
        self.request = self.screen()

    def screen(self):
        # read the image by name
        image_data = ImageQuerySet.read_image_by_name(
            image_name=self.image_to_compare, image_location=self.screen_name
        )
        # Assuming image_data.image_url contains the relative path or just the image name
        image_path = base_image_dir / image_data.image_url

        # Convert the path to an absolute path
        image_path = image_path.resolve()

        if image_data is None:
            raise AttributeError(
                f"Error: image_to_compare={self.image_to_compare} not found on screen_name={self.screen_name}"
            )
        try:
            start_time = time.time()
            screen_coords = pyautogui.locateOnScreen(
                image=str(image_path),
                minSearchTime=self.minSearchTime,
                confidence=self.confidence,
            )
            end_time = time.time()
            time_taken = end_time - start_time
        except Exception as e:
            print(e)
        if screen_coords is None:
            # TODO: add a screenshot here to capture the error with details
            logger.debug(
                {
                    "success": False,
                    "screen_coords": None,
                    "minSearchTime": self.minSearchTime,
                    "actual_time_taken": time_taken,
                    "image": image_path,
                }
            )
            response_data = {
                "success": False,
                "screen_coords": screen_coords,
                "minSearchTime": self.minSearchTime,
                "actual_time_taken": time_taken,
            }
            return Response(status_code=400, response_data=response_data)
        # raise ImageNotFound("Image not found")
        else:
            left, top, width, height = screen_coords
            right = left + width
            bottom = top + height
            center_x = left + width // 2
            center_y = top + height // 2
            _screen_coords = center_x, center_y

            # Convert tuple to a string representation
            region_str = f"({left}, {top}, {width}, {height})"

            # Extract screen coordinates
            x, y = _screen_coords

            # Simplified condition checks
            if self.mouse_click and not self.esc:
                if not self.skip_sleep:
                    # self.handle_mouse_click(x, y)
                    self.simulate_mouse(
                        x,
                        y,
                        mouse_click=self.mouse_click,
                        mouse_clicks=self.mouse_clicks,
                    )
                else:
                    # if skip_sleep is True, handle it here
                    # self.handle_mouse_click(x, y)
                    self.simulate_mouse(
                        x,
                        y,
                        mouse_click=self.mouse_click,
                        mouse_clicks=self.mouse_clicks,
                    )
                    pydirectinput.press("esc")
            elif self.skip_sleep:
                if self.esc:
                    pydirectinput.press("esc")

                sleep(random.uniform(0.10, 1.0))
            logger.debug(
                {
                    "success": True,
                    "screen_coords": _screen_coords,
                    "minSearchTime": self.minSearchTime,
                    "actual_time_taken": time_taken,
                    "image": image_path,
                }
            )
            response_data = {
                "success": True,
                "screen_coords": _screen_coords,
                "minSearchTime": self.minSearchTime,
                "actual_time_taken": time_taken,
            }
            return Response(status_code=200, response_data=response_data)


if __name__ == "__main__":
    verify = VerifyScreenMixin(
        screen_name="test1", skip_sleep=True, image_to_compare="testone"
    )
    try:
        var = verify.screen()
    except Exception as e:
        print(e)

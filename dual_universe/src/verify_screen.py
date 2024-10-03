import time
from abc import ABC, abstractmethod
from pathlib import Path

import pyautogui

from dual_universe.logs.logging_config import logger
from dual_universe.src.mouse_controller import MouseControllerMixin
from dual_universe.src.querysets.image_queryset import ImageQuerySet
from dual_universe.util.response import Response

# Define a base directory for all images
base_image_dir = Path(__file__).parent.parent


class ImageNotFound(Exception):
    """Custom exception class for image not found errors."""

    def __init__(self, message=None, error_code=None):
        super().__init__(message)
        self.error_code = error_code

    def __str__(self):
        if self.error_code is not None:
            return f"{super().__str__()} (Error Code: {self.error_code})"
        return super().__str__()


class ScreenMixinInterface(ABC):
    """Interface for screen-related actions."""

    @abstractmethod
    def screen(self, screen_name, image_to_compare, **kwargs):
        pass


class VerifyScreenMixin:
    """Class to verify images on the screen with optional mouse interactions."""

    def __init__(
        self,
        screen_name,
        image_to_compare,
        confidence=0.8,
        minSearchTime=3,
        mouse_clicks=0,
        skip_sleep=False,
        mouse_click=False,
        esc=False,
        mouse_mixin=MouseControllerMixin,
    ):
        self.screen_name = screen_name
        self.image_to_compare = image_to_compare
        self.confidence = confidence
        self.minSearchTime = minSearchTime
        self.mouse_clicks = mouse_clicks
        self.skip_sleep = skip_sleep
        self.mouse_click = mouse_click
        self.esc = esc
        self.mouse_mixin = mouse_mixin
        self.image_data = None
        self.screen_coords = None
        self.request = self.screen()

    def screen(self):
        """Perform screen verification and return the response."""
        self._get_image_data()

        start_time = time.time()
        self.screen_coords = self._locate_image_on_screen()
        time_taken = time.time() - start_time

        if self.screen_coords is None:
            return self._log_failure(time_taken)

        left, top, width, height = self.screen_coords
        center_x, center_y = left + width // 2, top + height // 2

        if self.mouse_click:
            self._simulate_mouse_click(center_x, center_y)
        return self._log_success(time_taken)

    def _get_image_data(self):
        """Fetch image data from the database or raise an error."""
        image_data = ImageQuerySet.read_image_by_name(
            image_name=self.image_to_compare, image_location=self.screen_name
        )
        if image_data is None:
            raise ImageNotFound(
                f"Image '{self.image_to_compare}' not found for screen '{self.screen_name}'"
            )
        self.image_data = (base_image_dir / image_data.image_url).resolve()

    def _locate_image_on_screen(self):
        """Attempt to locate the image on the screen using pyautogui."""
        try:
            return pyautogui.locateOnScreen(
                image=str(self.image_data),
                minSearchTime=self.minSearchTime,
                confidence=self.confidence,
            )
        except Exception as e:
            logger.error(f"Error during screen capture: {e}")
            return None

    def _log_failure(self, time_taken):
        """Log failure details and return an error response."""
        logger.debug(
            {
                "success": False,
                "screen_coords": self.screen_coords,
                "minSearchTime": self.minSearchTime,
                "actual_time_taken": time_taken,
                "image": self.image_data,
            }
        )
        response_data = {
            "success": False,
            "screen_coords": self.screen_coords,
            "minSearchTime": self.minSearchTime,
            "actual_time_taken": time_taken,
        }
        return Response(status_code=400, response_data=response_data)

    def _log_success(self, time_taken):
        """Log success details."""
        logger.debug(
            {
                "success": True,
                "screen_coords": self.screen_coords,
                "minSearchTime": self.minSearchTime,
                "actual_time_taken": time_taken,
                "image": self.image_data,
            }
        )
        response_data = {
            "success": True,
            "screen_coords": self.screen_coords,
            "minSearchTime": self.minSearchTime,
            "actual_time_taken": time_taken,
        }
        return Response(status_code=200, response_data=response_data)

    def _simulate_mouse_click(self, x, y):
        """Simulate a mouse click at the specified coordinates."""
        self.mouse_mixin.simulate_mouse(
            dest_x=x,
            dest_y=y,
            mouse_click=self.mouse_click,
            mouse_clicks=self.mouse_clicks,
        )


if __name__ == "__main__":
    try:
        verify = VerifyScreenMixin(
            screen_name="test1", skip_sleep=True, image_to_compare="testone"
        )
        var = verify.screen()
    except ImageNotFound as e:
        logger.error(f"Image not found: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

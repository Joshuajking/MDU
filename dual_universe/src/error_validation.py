import threading

from dual_universe.logs.logging_config import logger
from dual_universe.src.verify_screen import VerifyScreenMixin


class BatchErrorValidation:
    """used to validate multiple images at once with threading"""

    def __init__(self, screen_mixin=VerifyScreenMixin):
        self.screen_mixin = screen_mixin

    def _validate_internal_error(self):
        is_internal_error = self.screen_mixin(
            screen_name="ImageLocation.LOGIN_SCREEN",
            image_to_compare="internal_error",
            confidence=0.8,
            skip_sleep=True,
        )
        # checking if there is an internal error (incorrect email or password)
        return is_internal_error.request.status_code

    def _validate_gametime(self):
        # this one is tricky, we want to see a 400 code to indicate that there was no game time error
        is_gametime_error = self.screen_mixin(
            screen_name="ImageLocation.LOGIN_SCREEN",
            image_to_compare="gametime_error_lable",
            skip_sleep=True,
        )
        return is_gametime_error.request.status_code

    def _validate_email(self):
        # this one is tricky, we want to see a 400 code to indicate that there was no game time error
        is_email_error = self.screen_mixin(
            screen_name="ImageLocation.LOGIN_SCREEN",
            image_to_compare="invalid_email",
            skip_sleep=True,
        )
        return is_email_error.request.status_code

    def _validate_server(self):
        # this one is tricky, we want to see a 400 code to indicate that there was no game time error
        is_server_error = self.screen_mixin(
            screen_name="ImageLocation.LOGIN_SCREEN",
            image_to_compare="server_maintenance_lable",
            skip_sleep=True,
        )
        return is_server_error.request.status_code

    def _validate_password(self):
        # this one is tricky, we want to see a 400 code to indicate that there was no game time error
        is_password_error = self.screen_mixin(
            screen_name="ImageLocation.LOGIN_SCREEN",
            image_to_compare="password_error_lable",
            skip_sleep=True,
        )
        return is_password_error.request.status_code

    def validate_errors(self):
        """Run both validation functions concurrently and handle the results."""

        # results = [None, None, None, None, None]
        results = {
            "internal_error": None,
            "is_email_error": None,
            "is_server_error": None,
            "is_password_error": None,
            "gametime_error": None,
        }

        thread1 = threading.Thread(
            target=lambda: results.__setitem__(
                "internal_error", self._validate_internal_error()
            )
        )
        thread2 = threading.Thread(
            target=lambda: results.__setitem__(
                "gametime_error", self._validate_gametime()
            )
        )
        thread3 = threading.Thread(
            target=lambda: results.__setitem__("is_email_error", self._validate_email())
        )
        thread4 = threading.Thread(
            target=lambda: results.__setitem__(
                "is_server_error", self._validate_server()
            )
        )
        thread5 = threading.Thread(
            target=lambda: results.__setitem__(
                "is_password_error", self._validate_password()
            )
        )

        # Start both threads
        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()
        thread5.start()

        # Wait for both threads to finish
        thread1.join()
        thread2.join()
        thread3.join()
        thread4.join()
        thread5.join()

        return results

        # Now both tasks are complete, we can act on the results
        (
            internal_error_result,
            gametime_error_result,
            is_email_error,
            is_server_error,
            is_password_error,
        ) = results

        # Perform some action based on the results
        if internal_error == 200:
            logger.warning("Internal Server Error")
        if gametime_error == 200:
            logger.warning("Gametime Error")
        if is_email_error == 200:
            logger.warning("Email Error")
        if is_server_error == 200:
            logger.warning("Server Error")
        if is_password_error == 200:
            logger.warning("Password Error")

        if internal_error_result == 400:
            logger.success("No internal error")
        if gametime_error_result == 400:
            logger.success("No gametime error")
        if is_email_error == 400:
            logger.success("No email error")
        if is_server_error == 400:
            logger.success("No server error")
        if is_password_error == 400:
            logger.success("No password error")

        # You can return the results or handle them here
        # return (
        #     internal_error_result,
        #     gametime_error_result,
        #     is_email_error,
        #     is_server_error,
        #     is_password_error,
        # )

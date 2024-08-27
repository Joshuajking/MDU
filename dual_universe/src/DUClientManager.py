import subprocess
import time

import psutil
import pynput

from dual_universe.config.config_manager import ConfigMixin, timing_decorator
from dual_universe.logs.logging_config import logger
from models.models import ImageLocation
from dual_universe.src.verify_screen import VerifyScreenMixin


class DUClientManager(VerifyScreenMixin):
    def __init__(self):
        self.config_manager = ConfigMixin()
        self.game_client = self.config_manager.get_value("config.game_client")
        self.app_path = self.config_manager.get_value("config.app_path")
        self.DEBUG_MODE = self.is_debugging()
        self.mouse_listener = pynput.mouse.Listener(suppress=True)
        self.keyboard_listener = pynput.keyboard.Listener(suppress=True)

    def is_client_running(self) -> int:
        """Check if the game_client is running."""
        # TODO: Need to find an alternative to setting window to focus Windows has made to many restrictions on this
        # One thought would be to freeze mouse and keyboard control and then move the mouse to the client/game by image capture

        # self.mouse_listener.start()
        # self.keyboard_listener.start()

        pid = None
        list_of_processes = []
        geforce_client = "GeForceNOW.exe"
        du_client = "Dual.exe"
        for process in psutil.process_iter(["pid", "name", "create_time"]):
            list_of_processes.append(process)
            if process.info["name"] == self.game_client:
                pid = process.info["pid"]
                _start_time = process.info["create_time"]
                logger.debug(f"{self.game_client}: {process}, started at {_start_time}")
                break
        if not isinstance(pid, int):
            logger.debug(f"{self.game_client} not running, pid:{pid}")

        if not self.DEBUG_MODE:
            self.mouse_listener.stop()
            self.keyboard_listener.stop()

        return pid

    @timing_decorator
    def start_application(self):
        """Start the game_client application if not already running."""
        client_pid = self.is_client_running()
        if not isinstance(client_pid, int):
            try:
                # Start the application
                subprocess.Popen(self.app_path)
                logger.debug(f"Started game client: {self.app_path}")
            except Exception as e:
                logger.error(
                    f"Error while starting the application: {e}, {self.app_path}"
                )

            VerifyScreenMixin(
                screen_name=ImageLocation.LOGIN_SCREEN,
                image_to_compare="du_login_screen_label",
                verify_screen=True,
            )
            logger.success(f"game client started: {self.app_path}")

    def stop_application(self):
        """Stop the game_client application if running."""
        client_running = True
        while client_running:
            client_pid = self.is_client_running()
            if isinstance(client_pid, int):
                client_running = True
                logger.info("Client is running. Stopping...")
                try:
                    process = psutil.Process(client_pid)
                    process.terminate()
                    process.wait(timeout=5)
                    continue
                except psutil.TimeoutExpired:
                    process.kill()
                    continue
                except Exception as e:
                    logger.error(f"Error while stopping the application: {e}")
                    raise EnvironmentError(f"Error while stopping the application:")
            client_running = False
            logger.success(f"Client shutdown successfully")


if __name__ == "__main__":
    start_time = time.perf_counter()
    du_client = DUClientManager()
    du_client.start_application()
    du_client.stop_application()
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time}")
    pass

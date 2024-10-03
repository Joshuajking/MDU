import subprocess

import psutil

from dual_universe.config.config_manager import ConfigMixin
from dual_universe.src.models.image_model import ImageLocation
from dual_universe.src.verify_screen import VerifyScreenMixin


class SelfHostedClient:

    def __init__(self):
        hosted_client = "Dual.exe"
        self.path = "C:\ProgramData\My Dual Universe\dual-launcher.exe"

    def run(self):
        return self.path


class GeForceNowClient:

    def __init__(self):
        geforce_client = "GeForceNOW.exe"

    def run(self):
        pass


class DualUniverseDesktopClient:

    def __init__(self):
        self.du_client = "Dual.exe"

    def run(self):
        pass


class DualUniverseMyDuClient:
    def __init__(self):
        self.du_client = "dual-launcher.exe"
        self.path = "C:\ProgramData\My Dual Universe\dual-launcher.exe"

    def run(self):
        try:
            # Start the application
            subprocess.Popen(self.path)
        except Exception as e:
            print(e)

        du_launcher_screen = VerifyScreenMixin(
            screen_name=ImageLocation.LOGIN_SCREEN,
            image_to_compare="du_launcher_screen",
        )
        du_luncher_play_btn = VerifyScreenMixin(
            screen_name=ImageLocation.LOGIN_SCREEN,
            image_to_compare="du_luncher_play_btn",
            mouse_click=True,
        )
        my_du_login_screen = VerifyScreenMixin(
            screen_name=ImageLocation.LOGIN_SCREEN,
            image_to_compare="my_du_login_screen",
        )


class DualUniverseSteamClient:

    def __init__(self):
        du_client = "Dual.exe"
        self.path = "C:\Program Files (x86)\Steam\steamapps\common\Dual Universe\DualUniverse.exe"

    def run(self):
        return self.path


def run_client_class(result):
    class_map = {
        "geforcenow": GeForceNowClient,
        "steam": DualUniverseSteamClient,
        "desktop client": DualUniverseDesktopClient,
        "mydu": DualUniverseMyDuClient,
    }
    cls = class_map.get(result)
    if cls:
        instance = cls()
        return instance.run()
    else:
        return "No class found for given result"


class ClientManager:

    def __init__(self):
        pass

    def is_client_running(self) -> int:
        pid = None
        game_client = ["GeForceNOW.exe", "Dual.exe", "dual-launcher.exe"]

        # Iterate over all running processes with 'pid', 'name', and 'create_time'
        for process in psutil.process_iter(["pid", "name", "create_time"]):
            try:
                # Check if the process name is in the game_client list
                if process.info["name"] in game_client:
                    pid = process.info["pid"]
                    client_name = process.info["name"]
                    _start_time = process.info["create_time"]
                    print(
                        f"Game client running: {process.info['name']}, PID: {pid}, Start time: {_start_time}"
                    )
                    return pid  # Return the PID if a matching process is found
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                # Handle processes that no longer exist or are inaccessible
                continue

        return pid  # Return None if no matching process is found

    def start_application(self):
        """Start the game_client application if not already running."""
        from verify_screen import VerifyScreenMixin

        client_pid = self.is_client_running()
        if not isinstance(client_pid, int):
            config_manager = ConfigMixin()
            game_client = config_manager.get_value("config.game_client")
            path = run_client_class(game_client)
            try:
                # Start the application
                subprocess.Popen(path)
            except Exception as e:
                print(e)
        VerifyScreenMixin(
            screen_name=ImageLocation.LOGIN_SCREEN,
            image_to_compare="du_login_screen_label",
        )

    def stop_application(self):
        """Stop the game_client application if running."""
        client_running = True
        while client_running:
            client_pid = self.is_client_running()
            if isinstance(client_pid, int):
                client_running = True
                try:
                    process = psutil.Process(client_pid)
                    process.terminate()
                    process.wait(timeout=5)
                    continue
                except psutil.TimeoutExpired:
                    process.kill()
                    continue
                except Exception as e:
                    raise EnvironmentError(f"Error while stopping the application:")
            client_running = False


if __name__ == "__main__":
    pass

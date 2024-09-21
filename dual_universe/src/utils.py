import subprocess

import psutil

from dual_universe.src.models.image_model import ImageLocation


class SelfHostedClient:
    hosted_client = "Dual.exe"
    path = "C:\ProgramData\My Dual Universe\dual-launcher.exe"

    def __init__(self):
        pass


class GeForceNowClient:
    geforce_client = "GeForceNOW.exe"

    def __init__(self):
        pass


class DualUniverseDesktopClient:
    du_client = "Dual.exe"

    def __init__(self):
        pass


class DualUniverseSteamClient:
    du_client = "Dual.exe"
    path = "C:\Program Files (x86)\Steam\steamapps\common\Dual Universe\Bin\Dual.exe"

    def __init__(self):
        pass


class ClientManager:
    path = (
        "C:\Program Files (x86)\Steam\steamapps\common\Dual Universe\DualUniverse.exe"
    )

    def __init__(self):
        pass

    def is_client_running(self) -> int:
        pid = None
        game_client = ["GeForceNOW.exe", "Dual.exe"]

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
            try:
                # Start the application
                subprocess.Popen(self.path)
            except Exception as e:
                print(e)
        VerifyScreenMixin(
            screen_name=ImageLocation.LOGIN_SCREEN,
            image_to_compare="du_login_screen_label",
            verify_screen=True,
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
    obj = ClientManager()
    obj.start_application()
    obj.stop_application()

import psutil


class GeForceNowClient:
    geforce_client = "GeForceNOW.exe"

    def __init__(self):
        pass


class DualUniverseDesktopClient:
    du_client = "Dual.exe"

    def __init__(self):
        pass


class DualUniverseSteamClient:
    def __init__(self):
        pass


class ClientManager:
    def __init__(self):
        pass

    def is_client_running(self) -> int:
        pid = None
        list_of_processes = []
        for process in psutil.process_iter(["pid", "name", "create_time"]):
            list_of_processes.append(process)
            if process.info["name"] == self.game_client:
                pid = process.info["pid"]
                _start_time = process.info["create_time"]
                break
        if not isinstance(pid, int):
            pass

        return pid

def is_client_running(self) -> int:
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

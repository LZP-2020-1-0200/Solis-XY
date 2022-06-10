import logging
from pathlib import Path

import coloredlogs


class Logger:
    def __init__(self, module_name) -> None:
        self.logger = logging.getLogger(module_name)
        self.log_path = Path("solis.log")

        fh = logging.FileHandler(str(self.log_path))
        fh.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

        coloredlogs.install(level="INFO")

    def get_logger(self):
        return self.logger

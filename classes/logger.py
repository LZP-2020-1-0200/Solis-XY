import logging
from datetime import datetime
from getpass import getuser
from pathlib import Path

import coloredlogs


class Logger:
    def __init__(self, module_name) -> None:
        self.logger = logging.getLogger(module_name)
        self.log_path = Path(f"C://users//{getuser()}//Desktop//solis_{datetime.now().strftime('%Y-%m-%d')}.log")

        fh = logging.FileHandler(str(self.log_path))
        fh.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

        coloredlogs.install(level="INFO")

    def get_logger(self):
        return self.logger

import coloredlogs
import logging
from pywinauto import ElementNotFoundError
from pywinauto.application import Application
import pywinauto.keyboard as keyboard
from time import sleep


logger = logging.getLogger(__name__)
coloredlogs.install(level="INFO")

ALT = "%"
F5 = "{F5}"
CTRL = "^"
S = "S"
ENTER = "~"
DOWN = "{VK_DOWN}"
SPACE = "{VK_SPACE}"
F = "F"
A = "A"

# TODO redo this class with using toolbar if Solis supports
class Automatization:
    def __init__(self, title_regex: str) -> None:
        try:
            self.app: Application = Application().connect(title_re=title_regex)
            self.main_dlg = self.app.window(title_re=title_regex)
            self.success = True
            logger.info("Successfully attached to Andor Solis")
        except ElementNotFoundError:
            logger.error("Andor Solis is not detected ! Please open it first.")
            self.success = False

    def take_spectra(self, sleep_time: int):
        self.main_dlg.set_focus()
        keyboard.send_keys(F5)
        logger.info("Taking spectra...")
        sleep(sleep_time + 2)
        logger.info("Spectra taken")

    def save_spectra(self, filename: str, first_time: bool):
        self.main_dlg.set_focus()
        keyboard.send_keys(f"{CTRL}{S}")
        sleep(0.25)
        keyboard.send_keys(f"{filename.replace(' ',SPACE)}", pause=0.07)
        if first_time:
            logger.warning("There is 45 seconds to manually save first file")
            sleep(45)
        else:
            keyboard.send_keys(ENTER)
        # TODO test this
        logger.info(f"Spectra nr. {filename[:10]} saved")

    def close_saved_spectra(self):
        self.main_dlg.set_focus()
        keyboard.send_keys(f"{ALT}{F}{DOWN}{ENTER}")

    def capture_and_save(self, filename: str, integr_time: int, first_time: bool):
        self.take_spectra(integr_time)
        self.save_spectra(filename, first_time)
        self.close_saved_spectra()

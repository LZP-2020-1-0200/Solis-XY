import coloredlogs
import logging
from pywinauto import ElementNotFoundError
from pywinauto.application import Application, controls
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
            self.main_dlg: controls.hwndwrapper.DialogWrapper = self.app.window(title_re=title_regex)
            self.success = True
            logger.info("Successfully attached to Andor Solis")
        except ElementNotFoundError:
            logger.error("Andor Solis is not detected ! Please open it first.")
            self.success = False

    def take_spectra(self):
        self.main_dlg.set_focus()
        keyboard.send_keys(F5)
        logger.info("Taking spectra...")
        sleep(12)
        logger.info("Spectra taken")

    def save_spectra(self, filename: str, first_time: bool):
        self.main_dlg.set_focus()
        keyboard.send_keys(f"{CTRL}{S}{filename.replace(' ',SPACE)}")
        if first_time:
            logger.warning("There is 30 seconds to choose saving directory")
            sleep(30)
        else:
            keyboard.send_keys(ENTER)
        logger.info(f"Spectra nr.{filename.split('.')[1]}. saved")

    def close_saved_spectra(self):
        self.main_dlg.set_focus()
        keyboard.send_keys(f"{ALT}{F}{DOWN}{ENTER}")

    def capture_and_save(self, filename: str, first_time: bool = True):
        self.take_spectra()
        self.save_spectra(filename, first_time)
        self.close_saved_spectra()


if __name__ == "__main__":
    auto = Automatization()
    auto.connect_to_solis("Process Explorer - *")
    auto.save_spectra("vladislavs2", first_time=False)

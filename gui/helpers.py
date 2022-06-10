import PySimpleGUI as sg
from classes.logger import Logger

logger = Logger(__name__).get_logger()


def str_to_int(string: str):
    try:
        integer = int(string)
        return integer if integer != 0 else 1
    except ValueError:
        logger.error(f'Could not not convert "{string}" to Integer')
        return 0


def get_save_path():
    return sg.popup_get_file(message="", no_window=True, default_extension=".txt", save_as=True)


def get_load_path():
    return sg.popup_get_file(
        message="",
        no_window=True,
        file_types=(("TXT files", "*.txt"),),
    )


def disable_element(window: sg.Window, key: str):
    window[key].update(disabled=True)


def enable_element(window: sg.Window, key: str):
    window[key].update(disabled=False)

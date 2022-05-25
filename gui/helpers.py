import coloredlogs
import logging
import PySimpleGUI as sg


logger = logging.getLogger(__name__)
coloredlogs.install(level="INFO")


def str_to_int(string: str):
    try:
        return int(string)
    except ValueError:
        logger.error(f'Could not not convert "{string}" to Integer')


def get_save_path():
    return sg.popup_get_file(message="", no_window=1, default_extension=".txt", save_as=1)


def get_load_path():
    return sg.popup_get_file(
        message="",
        no_window=1,
        file_types=(("TXT files", "*.txt"),),
    )

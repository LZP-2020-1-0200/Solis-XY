import coloredlogs
import logging


logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO')


def str_to_int(string: str):
    try:
        return int(string)
    except ValueError:
        logger.error(f"Could not not convert \"{string}\" to Integer")


def refresh_com_ports():
    pass

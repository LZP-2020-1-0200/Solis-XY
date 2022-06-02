import coloredlogs
import logging
import PySimpleGUI as sg
import time

from classes.microscope_mover import MicroscopeMover, mover
from classes.scanner import Scanner
from classes.solis import Automatization
from gui.scanner_gui import AutomatizationGUI
from gui.helpers import get_load_path, str_to_int, disable_element

PADDING = 4

P_LETTER = ord("p"), ord("P")
S_LETTER = ord("s"), ord("S")


logger = logging.getLogger(__name__)
coloredlogs.install(level="INFO")

paused = False
stopped = False


def construct_number_with_padding(number: int):
    number_as_str = str(number)
    digit_count = len(number_as_str)
    return f"{'0'*(PADDING - digit_count)}{number_as_str}"


def start_scanning(
    scanner: Scanner, mover: MicroscopeMover, solis: Automatization, point_scans: int, integr_time: int
):
    global paused, stopped
    logger.info("Started scanning sequence")
    for i, point in enumerate(scanner.all_scanner_points):
        point_nr = construct_number_with_padding(i + 1)
        scanner.next_scan()
        mover.set_coordinates(point)
        for j in range(point_scans):

            while paused:
                time.sleep(0.5)
            if stopped:
                return

            solis.capture_and_save(
                filename=f"P{point_nr}_{j+1}", integr_time=integr_time, first_time=i == 0 and j == 0
            )

    logger.info("Successfully ended scanning sequence")


def main():
    global paused, stopped

    solis = Automatization("Andor SOLIS for Spectroscopy: *")

    if not solis.success:
        return

    gui = AutomatizationGUI()
    scanner = Scanner()
    window = gui.window

    while 1:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == "-LOADSCANPOINTS-":

            points_load_path = get_load_path()

            if not points_load_path:
                continue

            if not scanner.load_coordinates(points_load_path):
                continue

            window["-POINTCOUNT-"].update(scanner.all_point_count)
            disable_element(window, "-LOADSCANPOINTS-")

            stopped, paused = False, False

        if event == "-GOFIRSTPOINT-":

            if not scanner.all_scanner_points:
                logger.error("No scanning points loaded or submitted")
                continue

            mover.set_coordinates(scanner.all_scanner_points[0])

        if event == "-STARTSCAN-":

            if not scanner.all_scanner_points:
                logger.error("No scanning points loaded")
                continue

            scans_per_point = str_to_int(values["-NUMOFSCANS-"])

            if scans_per_point <= 0:
                logger.error("Negative number of scans")
                continue

            integration_time = str_to_int(values["-INTEGRATIONTIME-"])

            if integration_time <= 0:
                logger.error("Negative total integration time")
                continue

            window.perform_long_operation(
                lambda: start_scanning(scanner, mover, solis, scans_per_point, integration_time), "-SCANEND-"
            )

            disable_element(window, "-NUMOFSCANS-")
            disable_element(window, "-STARTSCAN-")
            disable_element(window, "-GOFIRSTPOINT-")

        if len(event) == 1 and ord(event) in P_LETTER:
            paused = True if not paused else False
            logger.warning("Paused Scanning" if paused else "Continue scanning")

        if len(event) == 1 and ord(event) in S_LETTER:
            stopped = True
            logger.warning("Abort scanning")


if __name__ == "__main__":
    main()

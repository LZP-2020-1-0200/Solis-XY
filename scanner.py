import coloredlogs
import logging
import PySimpleGUI as sg
import time

from classes.coordinate import Coordinate
from classes.microscope_mover import MicroscopeMover
from classes.scanner import Scanner, get_scanning_points
from classes.solis import Automatization
from gui.scanner_gui import AutomatizationGUI
import gui.buttons as btn
from gui.helpers import get_load_path, str_to_int, get_save_path, disable_element

PADDING = 7

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
    mover = MicroscopeMover()
    scanner = Scanner()
    window = gui.window

    points_of_interest: list[Coordinate] = []

    while 1:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == "-REFRESHCOMPORTS-":
            window["-COM_PORT_CHOOSER-"].Update(values=btn.get_available_com_ports())

        if event == "-CONNECT-":
            port_description = values["-COM_PORT_CHOOSER-"]
            com_port = btn.get_com_port_from_desc(port_description)

            if not mover.connect(com_port):
                continue

            disable_element(window, "-COM_PORT_CHOOSER-")
            disable_element(window, "-REFRESHCOMPORTS-")
            disable_element(window, "-CONNECT-")

        if event == "-ADDPOINTOFINT-":
            point = mover.get_coordinates()

            if not isinstance(point, Coordinate):
                continue

            points_of_interest.append(point)
            logger.info(f"Added point nr. {len(points_of_interest)}. with coordinates: {points_of_interest[-1]}")
            window["-CURRENTPOINTCOUNT-"].update(len(points_of_interest))

        if event == "-REMOVELAST-":

            if not len(points_of_interest):
                logger.error("List of points is empty!")
                continue

            logger.info(f"Removed point nr. {len(points_of_interest)}. with coordinates: {points_of_interest[-1]}")
            points_of_interest.pop()
            window["-CURRENTPOINTCOUNT-"].update(len(points_of_interest))

        if event == "-SUMBMISCANNO-":
            scans_count = str_to_int(values["-NUMBER_OF_SCANS-"])

            if scans_count <= 0:
                logger.error("Negative number of scans")
                continue

            if len(points_of_interest) < 2:
                logger.error(f"At least 2 points must be chosen! Current point count: {len(points_of_interest)}")
                continue

            scanning_points: list[Coordinate] = []
            for i in range(len(points_of_interest) - 1):
                between_points = get_scanning_points(points_of_interest[i], points_of_interest[i + 1], scans_count)

                if i == 0:
                    scanning_points.append(points_of_interest[0])

                for point in between_points:
                    scanning_points.append(point)

            scanner.set_points(scanning_points)
            logger.info("Points submitted successfully")
            window["-POINTCOUNT-"].update(len(scanning_points))

            stopped, paused = False, False

            disable_element(window, "-NUMBER_OF_SCANS-")
            disable_element(window, "-SUMBMISCANNO-")
            disable_element(window, "-ADDPOINTOFINT-")
            disable_element(window, "-REMOVELAST-")

        if event == "-SAVESCANPOINTS-":

            if not scanner.all_scanner_points:
                logger.error("No points for saving !")
                continue

            points_save_path = get_save_path()

            if not points_save_path:
                continue

            scanner.save_coordinate(points_save_path)

        if event == "-LOADSCANPOINTS-":

            points_load_path = get_load_path()

            if not points_load_path:
                continue

            if not scanner.load_coordinates(points_load_path):
                continue

            window["-POINTCOUNT-"].update(scanner.all_point_count)

            disable_element(window, "-NUMBER_OF_SCANS-")
            disable_element(window, "-SUMBMISCANNO-")
            disable_element(window, "-SAVESCANPOINTS-")
            disable_element(window, "-LOADSCANPOINTS-")
            disable_element(window, "-ADDPOINTOFINT-")
            disable_element(window, "-REMOVELAST-")

        if event == "-STARTSCAN-":

            if not scanner.all_scanner_points:
                logger.error("No scanning points loaded or submitted")
                continue

            if not mover.port_is_open():
                logger.error("Cannot start scanning: Microscope is not connected")
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

        if len(event) == 1 and ord(event) in P_LETTER:
            paused = True if not paused else False
            logger.warning("Paused Scanning" if paused else "Continue scanning")

        if len(event) == 1 and ord(event) in S_LETTER:
            stopped = True
            logger.warning("Abort scanning")


if __name__ == "__main__":
    main()

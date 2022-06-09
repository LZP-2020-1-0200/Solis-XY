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
current_point_nr = 1


def construct_number_with_padding(point_number: int, line_number: int):
    digit_count_point = len(str(point_number))
    digit_count_line = len(str(line_number))
    return f"P{'0'*(PADDING - digit_count_point)}{point_number}x{'0'*(PADDING - digit_count_line)}{line_number}"


def start_scanning(scanner: Scanner, mover: MicroscopeMover, solis: Automatization, integr_time: int):
    global paused, stopped, current_point_nr
    logger.info("Started scanning sequence")

    line_number = 0
    point_number = 1
    previous_x = 0
    one_point = True

    if len(scanner.all_scanner_points) >= 2:
        step = scanner.all_scanner_points[1] - scanner.all_scanner_points[0]
        one_point = False
        previous_x = 99999999 if step.x > 0 else -99999999

    for i, point in enumerate(scanner.all_scanner_points):
        current_point_nr = i + 1
        if not one_point:

            if step.x < 0 and point.x > previous_x:
                line_number += 1
                point_number = 1
            elif step.x > 0 and point.x < previous_x:
                line_number += 1
                point_number = 1

            previous_x = point.x

        point_filename = construct_number_with_padding(point_number, line_number)
        scanner.next_scan()
        mover.set_coordinates(point)

        while paused:
            time.sleep(0.5)

        if stopped:
            return

        solis.capture_and_save(filename=point_filename, integr_time=integr_time, first_time=i == 0)
        point_number += 1

    logger.info("Successfully ended scanning sequence")
    stopped, paused = False, False


def main():
    global paused, stopped, current_point_nr

    solis = Automatization("Andor SOLIS for Spectroscopy: *")

    if not solis.success:
        return

    gui = AutomatizationGUI()
    scanner = Scanner()
    window = gui.window

    started = False

    while 1:
        event, values = window.read(timeout=1000)

        if started:
            sg.one_line_progress_meter(
                "Progress bar",
                current_point_nr,
                len(scanner.all_scanner_points),
                orientation="h",
                keep_on_top=True,
                no_button=True,
            )

        if event == sg.WIN_CLOSED:
            break

        if event == "-LOADSCANPOINTS-":

            points_load_path = get_load_path()

            if not points_load_path:
                continue

            if not scanner.load_coordinates(points_load_path):
                continue

            window["-POINTCOUNT-"].update(scanner.all_point_count)
            stopped, paused = False, False

        if event == "-GOFIRSTPOINT-":

            if not scanner.all_scanner_points:
                logger.error("No scanning points loaded")
                continue

            mover.set_coordinates(scanner.all_scanner_points[0])

        if event == "-STARTSCAN-":

            if not scanner.all_scanner_points:
                logger.error("No scanning points loaded")
                continue

            integration_time = str_to_int(values["-INTEGRATIONTIME-"])

            if integration_time <= 0:
                logger.error("Negative total integration time")
                continue

            started = True

            window.perform_long_operation(lambda: start_scanning(scanner, mover, solis, integration_time), "-ENDSCAN-")
            disable_element(window, "-STARTSCAN-")

        if event == "-ENDSCAN-":
            started = False
            message = "Scanned stopped by user" if stopped else "Scanning successfully ended"
            color = "red" if stopped else "green"
            sg.one_line_progress_meter_cancel()
            sg.popup_ok(message, keep_on_top=True, background_color=color)

        if len(event) == 1 and ord(event) in P_LETTER:
            paused = True if not paused else False
            logger.warning("Paused Scanning" if paused else "Continue scanning")

        if len(event) == 1 and ord(event) in S_LETTER:
            stopped = True
            logger.warning("Abort scanning")


if __name__ == "__main__":
    main()

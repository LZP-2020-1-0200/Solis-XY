import coloredlogs
import logging
import PySimpleGUI as sg
from pathlib import Path

from classes.coordinate import Coordinate
from classes.microscope_mover import mover
from classes.scanner import Scanner, get_scanning_points
from gui.scanning_points_gui import ScannerPointsGUI
from gui.helpers import str_to_int, get_save_path


logger = logging.getLogger(__name__)
coloredlogs.install(level="INFO")

# TODO Add graphical representation
def main():
    height = Coordinate(0, 0)
    gui = ScannerPointsGUI()
    scanner = Scanner()
    window = gui.window

    points_of_interest: list[Coordinate] = []

    while 1:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == "-ADDPOINTOFINT-":

            if len(points_of_interest) == 2:
                logger.error("Max of 2 points")
                continue

            point = mover.get_coordinates()

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

        if event == "-GETHEIGHT-":

            if len(points_of_interest) != 2:
                logger.error("Firstly choose two points of interest")
                continue

            height = mover.get_coordinates()
            height = height - points_of_interest[-1]
            window["-HEIGHT-"].update(f"{height.y_qm} μm")

        if event == "-SUMBMISCANNO-":
            point_count = str_to_int(values["-NUMBER_OF_SCANS-"])

            if point_count <= 0:
                logger.error("Negative number of points")
                continue

            if len(points_of_interest) < 2:
                logger.error(f"At least 2 points must be chosen! Current point count: {len(points_of_interest)}")
                continue

            number_of_lines = str_to_int(values["-NUMOFLINES-"])

            if number_of_lines <= 0:
                logger.error("Negative number of lines")
                continue

            scanning_points: list[Coordinate] = []
            spacing = height / (number_of_lines - 1) if number_of_lines > 1 else Coordinate(0, 0)

            for i in range(number_of_lines):
                start_point = points_of_interest[0] + spacing * i
                end_point = points_of_interest[1] + spacing * i
                between_points = get_scanning_points(start_point, end_point, point_count)

                for point in between_points:
                    scanning_points.append(point)

            scanner.set_points(scanning_points)
            logger.info("Points submitted successfully")

        if event == "-SAVESCANPOINTS-":
            
            if not scanner.all_scanner_points:
                logger.error("No points for saving !")
                continue

            points_save_path = get_save_path()

            if not points_save_path:
                continue
            
            with open(Path(points_save_path).parent / "log.txt", "a") as file:
                file.write(f"Start point: {points_of_interest[0]}\n")
                file.write(f"End point: {points_of_interest[-1]}\n")
                file.write(f"Number of points per line: {point_count}\n")
                file.write(f"Number of lines: {number_of_lines}\n")

            scanner.save_coordinate(points_save_path)


if __name__ == "__main__":
    main()

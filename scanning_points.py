from pathlib import Path

import PySimpleGUI as sg

from classes.coordinate import Coordinate, read_all_points_from_file
from classes.logger import Logger
from classes.microscope_mover import mover
from classes.scanner import Scanner, get_scanning_points
from gui.helpers import get_load_path, get_save_path, str_to_int
from gui.scanning_points_gui import ScannerPointsGUI

logger = Logger(__name__).get_logger()


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

        if event == "-LOADPOINTS-":
            load_path = get_load_path()

            if not load_path:
                continue

            coordinates = read_all_points_from_file(load_path)

            if len(coordinates) != 2:
                logger.error(f"Wrong file, too much/little points ({len(coordinates)}), Expected: 2")
                continue

            points_of_interest = coordinates

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

            num_of_lines = str_to_int(values["-NUMOFLINES-"])

            if num_of_lines <= 0:
                logger.error("Negative number of lines")
                continue

            scanning_points: list[Coordinate] = []
            if num_of_lines > 1:
                spacing = Coordinate(height.x / (num_of_lines - 1), height.y / (num_of_lines - 1), rounding=False)
            else:
                spacing = Coordinate(0, 0)

            for i in range(num_of_lines):
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
                file.write(f"Number of lines: {num_of_lines}\n")

            scanner.save_coordinate(points_save_path)


if __name__ == "__main__":
    main()

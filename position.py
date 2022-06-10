import PySimpleGUI as sg

import gui.buttons as btn
from classes.coordinate import Coordinate, get_new_points, read_all_points_from_file, save_all_points_to_file
from classes.logger import Logger
from classes.microscope_mover import mover
from classes.scanner import Scanner
from gui.helpers import get_load_path, get_save_path, str_to_int
from gui.position_gui import CORNER_COUNT, PositionGUI, disable_step_elements

logger = Logger(__name__).get_logger()


def main():
    gui = PositionGUI()
    scanner = Scanner()
    window = gui.window

    points: dict[str, Coordinate] = {}

    while 1:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if "READ_COORD" in event:
            point = mover.get_coordinates()

            input_x = window[f"-S{event[2]}CORNER{event[-2]}_X-"]
            input_y = window[f"-S{event[2]}CORNER{event[-2]}_Y-"]

            btn.update_coordinate_inputs(input_x, input_y, point)

        if "GOTOCORD" in event:
            go_x = values[f"-S{event[2]}CORNER{event[-2]}_X-"]
            go_y = values[f"-S{event[2]}CORNER{event[-2]}_Y-"]

            go_x_int = str_to_int(go_x)
            go_y_int = str_to_int(go_y)

            if go_x_int == 0 or go_y_int == 0:
                continue

            go_cord = Coordinate(go_x_int, go_y_int)
            mover.set_coordinates(go_cord)

        if event == "-STEP1SUBMIT-":
            error_in_validation = False

            for i in range(1, CORNER_COUNT + 1):
                x = values[f"-S1CORNER{i}_X-"]
                y = values[f"-S1CORNER{i}_Y-"]

                x_int = str_to_int(x)
                y_int = str_to_int(y)

                if x_int == 0 or y_int == 0:
                    error_in_validation = True
                    break

                point_key = f"s1point{i}"
                points[point_key] = Coordinate(x_int, y_int)

            if error_in_validation:
                continue

            save_path = get_save_path()

            if not save_path:
                continue

            points_for_save = []
            for key in points:
                if "s1point" in key:
                    points_for_save.append(points[key])

            save_all_points_to_file(points_for_save, save_path)

            disable_step_elements(window, step=1)

        if event == "-STEP1LOAD-":
            load_path = get_load_path()

            if not load_path:
                continue

            coordinates = read_all_points_from_file(load_path)

            if len(coordinates) != CORNER_COUNT:
                logger.error(f"Wrong file, too much/little points ({len(coordinates)}), Expected: {CORNER_COUNT}")
                continue

            for i, coord in enumerate(coordinates):
                points[f"s1point{i+1}"] = coord
                input_x = window[f"-S1CORNER{i + 1}_X-"]
                input_y = window[f"-S1CORNER{i + 1}_Y-"]
                btn.update_coordinate_inputs(input_x, input_y, coord)

            disable_step_elements(window, step=1)

        if event == "-STEP2SUBMIT-":
            error_in_validation = False

            for i in range(1, CORNER_COUNT + 1):
                x = values[f"-S2CORNER{i}_X-"]
                y = values[f"-S2CORNER{i}_Y-"]

                x_int = str_to_int(x)
                y_int = str_to_int(y)

                if x_int == 0 or y_int == 0:
                    error_in_validation = True
                    break

                point_key = f"s2point{i}"
                points[point_key] = Coordinate(x_int, y_int)

            if error_in_validation:
                continue

            save_path = get_save_path()
            if not save_path:
                continue

            points_for_save = []
            for key in points:
                if "s2point" in key:
                    points_for_save.append(points[key])

            save_all_points_to_file(points_for_save, save_path)

            disable_step_elements(window, step=2)

        if event == "-CONVERTPOINTS-":

            error_in_validation = False

            for i in range(1, CORNER_COUNT + 1):
                if f"s1point{i}" not in points:
                    logger.error(f"{i}. initial corner is missing")
                    error_in_validation = True
                    break

            for i in range(1, CORNER_COUNT + 1):
                if f"s2point{i}" not in points:
                    logger.error(f"{i}. new corner is missing")
                    error_in_validation = True
                    break

            if error_in_validation:
                continue

            points_load_path = get_load_path()

            if not points_load_path:
                continue

            scanner.load_coordinates(points_load_path)

            old_corners = sorted([points["s1point1"], points["s1point2"]])
            new_corners = sorted([points["s2point1"], points["s2point2"]])

            new_points = get_new_points(scanner.all_scanner_points, old_corners, new_corners)

            scanner.set_points(new_points)
            scanner.save_coordinate(points_load_path[:-4] + "_new.txt")

        if event == "-SAMEVALUES-":

            error_in_validation = False

            for i in range(1, CORNER_COUNT + 1):
                if f"s1point{i}" not in points:
                    logger.error(f"{i}. initial corner is missing")
                    error_in_validation = True
                    break

            if error_in_validation:
                continue

            for i in range(1, CORNER_COUNT + 1):
                points[f"s2point{i}"] = points[f"s1point{i}"]
                input_x = window[f"-S2CORNER{i}_X-"]
                input_y = window[f"-S2CORNER{i}_Y-"]
                btn.update_coordinate_inputs(input_x, input_y, points[f"s2point{i}"])


if __name__ == "__main__":
    main()

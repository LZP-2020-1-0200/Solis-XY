from __future__ import annotations
from math import atan2, degrees, sin, cos, radians
import coloredlogs
import logging
import csv

logger = logging.getLogger(__name__)
coloredlogs.install(level="INFO")
coloredlogs.install(level="INFO", logger=logger)


UNIT_TO_NANOMETER = 40
NM_TO_QM = 1000


def get_rotation(btm_point: Coordinate, top_point: Coordinate) -> float:
    """Gets rotation angle in degrees

    Args:
        pnt1 (Coordinate): Bottom corner of line
        pnt2 (Coordinate): Top corner of line

    Returns:
        float: Rotation in degrees
    """
    corner_length = top_point - btm_point
    rotation = atan2(corner_length.y, corner_length.x)
    return degrees(rotation)


def rotate_point(point: Coordinate, angle: int | float) -> Coordinate:
    rad_angle = radians(angle)
    new_x = point.x * cos(rad_angle) - point.y * sin(rad_angle)
    new_y = point.x * sin(rad_angle) + point.y * cos(rad_angle)
    return Coordinate(new_x, new_y)


def get_translation(initial_point: Coordinate, new_point: Coordinate, angle: int | float = 0) -> Coordinate:
    rad_angle = radians(angle)
    x_transl = -initial_point.x * cos(rad_angle) + initial_point.y * sin(rad_angle) + new_point.x
    y_transl = -initial_point.x * sin(rad_angle) - initial_point.y * cos(rad_angle) + new_point.y
    return Coordinate(x_transl, y_transl)


def get_new_points(
    old_points: list[Coordinate],
    old_corners: list[Coordinate],
    new_corners: list[Coordinate],
):
    """Returns new points of interest based on rotation and/or translation of new corners

    Args:
        old_points (list[Coordinate]): List of old point of interest
        old_corners (list[Coordinate]): Sorted list of old corners
        new_corners (list[Coordinate]): Sorted list of new corners

    Returns:
        list[Coordinate]: List of new calculated points
    """
    new_points: list[Coordinate] = []
    # Get total rotation from both new and old corners
    rotation_old = get_rotation(old_corners[0], old_corners[1])
    rotation_new = get_rotation(new_corners[0], new_corners[1])
    total_rotation = rotation_new - rotation_old

    # Calculate translation using old corner points and new corner points
    translation1 = get_translation(old_corners[0], new_corners[0], total_rotation)
    translation2 = get_translation(old_corners[1], new_corners[1], total_rotation)
    average_translation = (translation1 + translation2) / 2

    for point in old_points:
        # Generate rotated point from rotation and old point
        point_rotated = rotate_point(point, total_rotation)
        # Calculate new rotated and/or translated point
        new_point = point_rotated + average_translation
        new_points.append(new_point)

    return new_points


def read_all_points_from_file(path_to_file: str):
    with open(path_to_file, "r") as file:
        list_of_coordinates: list[Coordinate] = []
        csv_reader = csv.reader(file, delimiter=",")
        for i, row in enumerate(csv_reader):
            if len(row) > 2:
                logger.error(f"Wrong file, more than 2 columns detected ! ({len(row)}) ")
                return []
            try:
                x = int(row[0])
                y = int(row[1])
            except ValueError as e:
                logger.error(f"Could not convert{e.args[0].split(':')[-1]} at line: {i+1} to Integer")
                return []

            coordinate = Coordinate(x, y)
            list_of_coordinates.append(coordinate)
        logger.info(f"Successfully loaded all points")
        return list_of_coordinates


def save_all_points_to_file(points: list[Coordinate], path: str):
    with open(path, "w", newline="") as file:
        csv_writer = csv.writer(file, delimiter=",")
        for point in points:
            csv_writer.writerow(point.tuple)
    logger.info(f"Successfully saved points at {path}")


class Coordinate:
    def __init__(self, x: int | float, y: int | float):

        x_ = round(x)
        y_ = round(y)

        self.x = x_
        self.y = y_

        self.x_qm = self.x * UNIT_TO_NANOMETER / NM_TO_QM
        self.y_qm = self.y * UNIT_TO_NANOMETER / NM_TO_QM

        self.tuple = self.x, self.y
        self.tuple_qm = self.x_qm, self.y_qm

    def __str__(self):
        return f"X: {self.x} Y: {self.y}"

    def __add__(self, other: Coordinate):
        return Coordinate(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Coordinate):
        return Coordinate(self.x - other.x, self.y - other.y)

    def __mul__(self, multiplier: int | float):
        return Coordinate(self.x * multiplier, self.y * multiplier)

    def __truediv__(self, divider: int | float):
        return Coordinate(self.x / divider, self.y / divider)

    def __eq__(self, other: Coordinate):
        return self.x == other.x and self.y == other.y

    def __abs__(self):
        return Coordinate(abs(self.x), abs(self.y))

    def __lt__(self, other: Coordinate):
        return (self.y) < (other.y)

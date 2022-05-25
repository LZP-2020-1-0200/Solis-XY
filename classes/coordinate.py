from __future__ import annotations
from math import atan2, sin, cos, radians, pi
import coloredlogs
import logging

logger = logging.getLogger(__name__)
coloredlogs.install(level="INFO")
coloredlogs.install(level="INFO", logger=logger)


UNIT_TO_NANOMETER = 40
NM_TO_QM = 1000


def get_rotation(btm_point: Coordinate, top_point: Coordinate, edge: str = "left") -> float:
    """Gets rotation angle in degrees

    Args:
        pnt1 (Coordinate): Bottom corner of line
        pnt2 (Coordinate): Top corner of line
        edge {'left', 'top', 'right', 'bottom'}, optional: Side of edge. Defaults to "left".

    Returns:
        float: Rotation in degrees
    """
    if edge not in ["left", "right", "bottom", "top"]:
        raise TypeError(f'Not possible edge value "{edge}" ')
    offset = 0
    match edge:
        case "top":
            offset = 90
        case "right":
            offset = 180
        case "bottom":
            offset = 90

    corner_length = top_point - btm_point
    rotation = atan2(*corner_length.tuple)
    return rotation * 180 / pi * -1 + offset


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


def get_new_point(
    old_point: Coordinate, old_corner: Coordinate, new_corner_btm: Coordinate, new_corner_top: Coordinate, btm=True
) -> Coordinate:
    """Generate new point based on rotation and translation

    Args:
        old_point (Coordinate): Old point of interest
        old_corner (Coordinate): Initial corner point
        new_corner_btm (Coordinate): New corner bottom point
        new_corner_top (Coordinate): New corner top point
        btm (bool, optional): True if new corner is line's bottom point else False. Defaults to bottom.

    Returns:
        Coordinate: New point based on rotation and translation
    """
    # Get rotation from new corners
    rotation = get_rotation(new_corner_btm, new_corner_top)
    # Generate rotated point from rotation and old point
    old_point_rotated = rotate_point(old_point, rotation)
    # Calculate translation using old corner point and new corner point
    if btm:
        translation = get_translation(old_corner, new_corner_btm, rotation)
    else:
        translation = get_translation(old_corner, new_corner_top, rotation)
    # Return rotated and/or translated point
    return old_point_rotated + translation


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


# test
if __name__ == "__main__":

    btm = Coordinate(1.74, 2.23)
    top = Coordinate(1.13, 7.2)

    points = [btm, top]

    print(max(points))

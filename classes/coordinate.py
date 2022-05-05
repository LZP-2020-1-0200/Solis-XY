from __future__ import annotations
from operator import itemgetter

UNIT_TO_NANOMETER = 40
NM_TO_QM = 1000


class Coordinate:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

        self.x_nm = coordinate_unit_to_qm(x)
        self.y_nm = coordinate_unit_to_qm(y)

        self.tuple = (self.x, self.y)
        self.tuple_nm = (self.x_nm, self.y_nm)

    def coord_to_tuple(self):
        return self.x, self.y

    def add(self, coord_to_add: Coordinate) -> Coordinate:
        return Coordinate(self.x + coord_to_add.x, self.y + coord_to_add.y)

    def subtract(self, coordinate: Coordinate) -> Coordinate:
        return Coordinate(self.x - coordinate.x, self.y - coordinate.y)

    def divide(self, divider: int | float, ) -> Coordinate:
        return Coordinate(round(self.x / divider), round(self.y / divider))

    def multiply(self, multiplier: int | float) -> Coordinate:
        return Coordinate(self.x * multiplier, self.y * multiplier)

    def __str__(self):
        return f"X: {self.x} Y: {self.y}"


def coordinate_unit_to_qm(coordinate: int) -> int:
    """Converts coordinate unit to micrometer unit

    Args:
        coordinate (int): Raw data from controlller with unknown units

    Returns:
        int: Micrometer
    """
    return round(coordinate * UNIT_TO_NANOMETER / NM_TO_QM)


def coordinate_nm_to_unit(coordinate: int) -> int:
    return round(coordinate / UNIT_TO_NANOMETER * NM_TO_QM)


def coordinate_to_list(*coordinates):
    return [(cord.x, cord.y) for cord in coordinates]


def find_min_max(corners):
    x_min = min(corners, key=itemgetter(0))[0]
    y_min = min(corners, key=itemgetter(1))[1]

    x_max = max(corners, key=itemgetter(0))[0]
    y_max = max(corners, key=itemgetter(1))[1]

    return x_min, y_min, x_max, y_max

from __future__ import annotations
import coloredlogs
import logging

logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO')
coloredlogs.install(level='INFO', logger=logger)


UNIT_TO_NANOMETER = 40
NM_TO_QM = 1000


class Coordinate:

    def __init__(self, x: int | float, y: int | float):
        x_, y_ = round(x), round(y)

        self.x = x_
        self.y = y_

        self.x_qm = self.x * UNIT_TO_NANOMETER / NM_TO_QM
        self.y_qm = self.y * UNIT_TO_NANOMETER / NM_TO_QM

        self.tuple = self.x, self.y
        self.tuple_qm = self.x_qm, self.y_qm
        
        # logger.info(f"Created coordinate with X: {self.x} Y: {self.y}")

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

    # def coord_to_tuple(self):
    #     return self.x, self.y

    # def add(self, coord_to_add: Coordinate) -> Coordinate:
    #     return Coordinate(self.x + coord_to_add.x, self.y + coord_to_add.y)

    # def subtract(self, coordinate: Coordinate) -> Coordinate:
    #     return Coordinate(self.x - coordinate.x, self.y - coordinate.y)

    # def divide(self, divider: int | float, ) -> Coordinate:
    #     return Coordinate(round(self.x / divider), round(self.y / divider))

    # def multiply(self, multiplier: int | float) -> Coordinate:
    #     return Coordinate(self.x * multiplier, self.y * multiplier)


# def coordinate_unit_to_qm(coordinate: int) -> int:
#     """Converts coordinate unit to micrometer unit

#     Args:
#         coordinate (int): Raw data from controlller with unknown units

#     Returns:
#         int: Micrometer
#     """
#     return round(coordinate * UNIT_TO_NANOMETER / NM_TO_QM)


# def coordinate_nm_to_unit(coordinate: int | float) -> float:
#     return coordinate / UNIT_TO_NANOMETER * NM_TO_QM


# def coordinate_to_list(*coordinates):
#     return [(cord.x, cord.y) for cord in coordinates]


# def find_min_max(corners):
#     x_min = min(corners, key=itemgetter(0))[0]
#     y_min = min(corners, key=itemgetter(1))[1]

#     x_max = max(corners, key=itemgetter(0))[0]
#     y_max = max(corners, key=itemgetter(1))[1]

#     return x_min, y_min, x_max, y_max


# test
if __name__ == "__main__":
    coord1 = Coordinate(100, 253)
    cord2 = Coordinate(221, 1321)

    cord3 = cord2 / 3
    # print(coord1, cord2, cord3)

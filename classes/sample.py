import coloredlogs
import logging
import csv
import math

from classes.coordinate import Coordinate
# testing
# from coordinate import Coordinate

logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO')
coloredlogs.install(level='INFO', logger=logger)


def get_scanning_points_from_points(pnt1: Coordinate, pnt2: Coordinate, nb_points: int):
    spacing = (pnt2 - pnt1) / (nb_points + 1)
    all_points = [pnt1 + spacing * i for i in range(1, nb_points + 1)]
    all_points.append(pnt2)
    return all_points


class Sample:

    def __init__(self, *corners: tuple[Coordinate]):
        # todo rewrite this class completley
        self.left_btm_corner = corners[0]
        self.left_top_corner = corners[1]
        self.right_btm_corner = corners[3]
        self.right_top_corner = corners[2]

        self.corners_list = [self.left_btm_corner, self.left_top_corner,
                             self.right_top_corner, self.right_btm_corner]

        self.left_edge_length = (
            self.left_top_corner.subtract(self.left_btm_corner)).y
        self.right_edge_length = (
            self.right_top_corner.subtract(self.right_btm_corner)).y
        self.top_edge_length = (
            self.right_top_corner.subtract(self.left_top_corner)).x
        self.btm_edge_length = (
            self.right_btm_corner.subtract(self.left_btm_corner)).x

        self.y_center_left = self.left_btm_corner.add(
            self.left_top_corner).divide(2)
        self.y_center_right = self.right_btm_corner.add(
            self.right_top_corner).divide(2)

        self.center = self.left_btm_corner.add(self.right_top_corner).divide(2)
        # print("x,y center: ", self.y_center_right, self.y_center_left)

        self.rotation_angle = self.get_rotation()

    def get_rotation(self) -> float:
        length = self.left_top_corner.subtract(self.left_btm_corner)
        rotation = math.atan2(*length.tuple)
        return rotation * 180 / math.pi * -1

    def save_corners(self, path):
        # print(path)
        with open(path, "w", newline='') as file:
            csvReader = csv.writer(file, delimiter=",")
            for corner in self.corners_list:
                csvReader.writerow(list(corner.tuple))

    def __str__(self):
        return (
            f"{self.left_top_corner.x},{self.left_top_corner.y}---------------{self.right_top_corner.x},"
            f"{self.right_top_corner.y}\n{self.left_btm_corner.x},{self.left_btm_corner.y}---------------"
            f"{self.right_btm_corner.x},{self.right_btm_corner.y}")

    def all_x(self):
        return [self.left_btm_corner.x, self.left_top_corner.x,
                self.right_top_corner.x, self.right_btm_corner.x,
                self.left_btm_corner.x]

    def all_y(self):
        return [self.left_btm_corner.y, self.left_top_corner.y,
                self.right_top_corner.y, self.right_btm_corner.y,
                self.left_btm_corner.y]

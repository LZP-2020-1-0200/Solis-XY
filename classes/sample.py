from classes.coordinate import Coordinate
import math


# from operator import itemgetter
# def find_corners(corners):
#     x_min = min(corners, key=itemgetter(0))[0]
#     y_min = min(corners, key=itemgetter(1))[1]

#     x_max = max(corners, key=itemgetter(0))[0]
#     y_max = max(corners, key=itemgetter(1))[1]

#     return (x_min, y_min), (x_min, y_max), (x_max, y_min), (x_max, y_max)

class Sample:

    def __init__(self, *corners):
        self.left_btm_corner = corners[0]
        self.left_top_corner = corners[1]
        self.right_btm_corner = corners[3]
        self.right_top_corner = corners[2]

        self.left_edge_length = (self.left_top_corner.subtract(self.left_btm_corner)).y
        self.right_edge_length = (self.right_top_corner.subtract(self.right_btm_corner)).y
        self.top_edge_length = (self.right_top_corner.subtract(self.left_top_corner)).x
        self.btm_edge_length = (self.right_btm_corner.subtract(self.left_btm_corner)).x

        self.top_edge_length = self.right_top_corner.x - self.left_top_corner.x
        self.btm_edge_length = self.right_btm_corner.x - self.left_btm_corner.x

        self.y_center_left = self.left_btm_corner.add(self.left_top_corner).divide(2)
        self.y_center_right = self.right_btm_corner.add(self.right_top_corner).divide(2)

        self.center = self.left_btm_corner.add(self.right_top_corner).divide(2)
        print("x,y center: ", self.y_center_right, self.y_center_left)

        self.rotation_angle = self.get_rotation()

    def get_scanning_points_from_center(self, nb_points: int) -> list[Coordinate]:
        """"Return a list of nb_points equally spaced points
        between p1 and p2"""
        spacing = self.y_center_right.subtract(self.y_center_left).divide(nb_points + 1)
        return [self.y_center_left.add(spacing.multiply(i)) for i in range(1, nb_points + 1)]

    def get_rotation(self) -> float:
        length = self.left_top_corner.subtract(self.left_btm_corner)
        rotation = math.atan2(*length.tuple)
        return rotation * 180 / math.pi * -1

    def __str__(self):
        return (
            f"{self.left_top_corner.x},{self.left_top_corner.y}---------------{self.right_top_corner.x},"
            f"{self.right_top_corner.y}\n{self.left_btm_corner.x},{self.left_btm_corner.y}---------------"
            f"{self.right_btm_corner.x},{self.right_btm_corner.y}")
        # self.y_center[0] + i * x_spacing, p1[1] +  i * y_spacing]

# print(intermediates([1, 2], [10, 6.5], nb_points=8))

# [[2.0, 2.5], [3.0, 3.0], [4.0, 3.5], [5.0, 4.0], 
#  [6.0, 4.5], [7.0, 5.0], [8.0, 5.5], [9.0, 6.0]]


# self.left_edge = self.left_top_corner.substract_y(self.left_btm_corner.y)
# self.top_edge = self.right_top_corner.substract_x(self.left_top_corner.x)
# self.right_edge = self.right_top_corner.substract_y(self.right_btm_corner.y)
# self.btm_edge = self.right_btm_corner.substract_x(self.left_btm_corner.x)

# self.left_edge_length =

# self.top_edge = self.

import PySimpleGUI as sg
from matplotlib.ticker import NullFormatter  # useful for `logit` scale
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import matplotlib
from matplotlib.patches import Rectangle
from operator import itemgetter

def find_corners(corners):
    x_min = min(corners,key=itemgetter(0))[0]
    x_max = max(corners, key=itemgetter(0))[0]
    y_min = min(corners, key=itemgetter(1))[1]
    y_max = max(corners, key=itemgetter(1))[1]

    print(x_min,x_max,y_min,y_max)

    corners.sort(key=lambda x: x[0] + x[1])
    return corners


if __name__ == "__main__":
    all_corners = [(12, 27), (18, 21), (12, 21), (18, 27)]
    left_btm_corner, left_top_corner, right_btm_corner, right_top_corner = find_corners(all_corners)


# print(find_left_btm_corner(all_corners))
# print(all_corners)
#
# def calculate_relative_coordinates(coord1, coord2):
#     return coord1[0] - coord2[0], coord1[1] - coord2[1]
#
#
# print(calculate_relative_coordinates(corner1_start, corner2_start))
# print(find_corner_position())
# fig, ax = plt.subplots()
#
# # create simple line plot
# # add rectangle to plot
# ax.add_patch(Rectangle((1, 1), 2, 6))
#
# # display plot
# plt.show()

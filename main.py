import numpy as np

from classes.coordinate import Coordinate
from classes.sample import get_scanning_points_from_points, Sample
from classes.microscope_mover import MicroscopeMover
from gui.gui import GUI
from gui.plot_gui import PlotGUI, set_visible, points_of_interest
from classes.scanner import Scanner
import gui.buttons as buttons
from matplotlib.patches import Rectangle as Rectangle_
import PySimpleGUI as sg
import csv

without_saving = True

if __name__ == "__main__":
    window = GUI().window

    plot_gui = PlotGUI()
    plot_window = plot_gui.window
    axes, fig_agg, initial, final = plot_gui.ax, plot_gui.fig_agg, plot_gui.initial, plot_gui.final
    scatter_points, cur_point = plot_gui.points, plot_gui.current_points

    while True:
        window, event, values = sg.read_all_windows()
        if event == sg.WIN_CLOSED:  # if user closes window or clicks cancel
            break

        if event == "-REFRESHCOMPORTS-":
            window["-COM_PORT_CHOOSER-"].Update(values=buttons.get_available_com_ports())

        if event == "-CONNECT-":
            # print(type(buttons.get_com_port_from_desc(values["-COM_PORT_CHOOSER-"])))
            mover = MicroscopeMover(buttons.get_com_port_from_desc(values["-COM_PORT_CHOOSER-"]))

        if "READ_COORD" in event:
            # todo add error pop-up
            try:
                new_values = mover.get_coordinates()
                buttons.update_coordinate_inputs(window[f"-S{event[2]}CORNER{event[-2]}_X-"],
                                                 window[f"-S{event[2]}CORNER{event[-2]}_Y-"],
                                                 new_values)
            except Exception as e:
                print(e)

        if "GOTOCORD" in event:
            # print(event)

            print(f"-S{event[2]}CORNER{event[-2]}_X-")
            try:
                mover.set_coordinates(window[f"-S{event[2]}CORNER{event[-2]}_X-"], window[f"-S{event[2]}CORNE"
                                                                                          f"R{event[-2]}_Y-"])
            except NameError:
                print("Microscope is not connected!")

        if event == "-STEP1SUBMIT-":
            # todo add error handling
            save_path = sg.popup_get_file("", no_window=1, default_extension=".txt", save_as=1)
            if save_path:
                initial_sample.save_corners(save_path)

            initial_sample = Sample(
                *[Coordinate(int(values[f"-S1CORNER{i}_X-"]), int(values[f"-S1CORNER{i}_Y-"])) for i in range(1, 5)])

            axes.set_xlim(initial_sample.left_btm_corner.x - (initial_sample.left_btm_corner.x / 4),
                          initial_sample.right_top_corner.x + (initial_sample.left_btm_corner.x / 4))
            axes.set_ylim(initial_sample.left_btm_corner.y - (initial_sample.left_btm_corner.y / 4),
                          initial_sample.right_top_corner.y + (initial_sample.right_top_corner.y / 4))
            initial.set_data(initial_sample.all_x(), initial_sample.all_y())
            fig_agg.draw()

        if event == "-STEP1LOAD-":
            file = sg.popup_get_file("", no_window=1, file_types=(("TXT files", "*.txt"),), )
            if not file:
                continue

            with open(file) as file2:
                csvReader = csv.reader(file2, delimiter=",")
                for i, row in enumerate(csvReader):
                    print(row)
                    buttons.update_coordinate_inputs(window[f"-S1CORNER{i + 1}_X-"],
                                                     window[f"-S1CORNER{i + 1}_Y-"],
                                                     [row[0], row[1]])

        if event == "-STEP2SUBMIT-":
            # todo add error handling
            save_path2 = sg.popup_get_file("", no_window=1, default_extension=".txt", save_as=1)

            final_sample = Sample(*[Coordinate(int(values[f"-S2CORNER{i}_X-"]), int(values[f"-S2CORNER{i}_Y-"])) for i in range(1, 5)])

            nobide = final_sample.left_btm_corner.subtract(initial_sample.left_btm_corner)
            nobide2 = final_sample.left_top_corner.subtract(initial_sample.left_top_corner)
            nobide3 = final_sample.right_top_corner.subtract(initial_sample.right_top_corner)
            nobide4 = final_sample.right_btm_corner.subtract(initial_sample.right_btm_corner)

            print(nobide,nobide3,nobide4)

            if save_path2:
                final_sample.save_corners(save_path2)

            final.set_data(final_sample.all_x(), final_sample.all_y())
            fig_agg.draw()

        if event == "-SAMEVALUES-":

            a = [(int(values[f"-S1CORNER{i}_X-"]), int(values[f"-S1CORNER{i}_Y-"])) for i in range(1, 5)]
            for i in range(1, 5):
                # todo change back
                window[f"-S2CORNER{i}_X-"].update(a[i - 1][0]-16745)
                window[f"-S2CORNER{i}_Y-"].update(a[i - 1][1]+35551)

        if event == "-NUMBER_OF_SCANS-":
            try:
                num_of_scans = int(values["-NUMBER_OF_SCANS-"])
            except:
                num_of_scans = 0
            scatter_points.set_data([], [])
            fig_agg.draw()
            # todo error handling
            # a = len(points_of_interest)
            all_trajectory = []
            i = 0
            while i < len(points_of_interest) - 1:
                all_trajectory.append(
                    get_scanning_points_from_points(points_of_interest[i], points_of_interest[i + 1], num_of_scans))
                i += 1

            all_trajectory = np.array(all_trajectory).flatten()

            # for x in all_trajectory:
            #     print(x)

            xx = [x.x for x in all_trajectory]
            yy = [y.y for y in all_trajectory]

            scatter_points.set_data(xx, yy)
            fig_agg.draw()

            scanner = Scanner(all_trajectory)

            # try:
            #     scanning_point_count = int(values["-NUMBER_OF_SCANS-"])
            #     scanner = Scanner(final_sample.get_scanning_points_from_center(scanning_point_count))
            #     scatter_points.set_data(scanner.list_of_x_coord(), scanner.list_of_y_coord())
            #     fig_agg.draw()
            # except ValueError:
            #     scanning_point_count = 1

        if event == "-SUMBMISCANNO-":
            scanner.next_scan()
            mover.set_coordinates(*scanner.current_point_coord.tuple)
            cur_point.set_data(*scanner.current_point_coord.tuple)
            window["-SCANNO-"].update(str(scanner.current_point_no + 1))
            window["-CURRENTXY-"].update(str(scanner.current_point_coord))

        if event == "-PREVIOUS-" or event == "-NEXT-":
            scanner.previous_scan() if event == "-PREVIOUS-" else scanner.next_scan()
            mover.set_coordinates(*scanner.current_point_coord.tuple)
            cur_point.set_data(*scanner.current_point_coord.tuple)
            fig_agg.draw()
            window["-SCANNO-"].update(str(scanner.current_point_no + 1))
            window["-CURRENTXY-"].update(str(scanner.current_point_coord))

        if event == "-SAVESCANPOINTS-":
            points_save_path = sg.popup_get_file("", no_window=1, default_extension=".txt", save_as=1)
            if points_save_path:
                scanner.save_coordinate(points_save_path)
                points_save_path = None

        if event == "-LOADSCANPOINTS-":
            points_load_path = sg.popup_get_file("", no_window=1, default_extension=".txt")
            if points_load_path:
                scanner = Scanner([])
                scanner.load_coordinates(points_load_path)
                points_load_path = None
            xx = [x.x + nobide.x for x in scanner.all_scanner_points]
            yy = [y.y + nobide.y for y in scanner.all_scanner_points]
            scatter_points.set_data(xx, yy)
            fig_agg.draw()

        # plot gui events
        if event == "-SHOW_FIRST-":
            set_visible(initial, values[event], fig_agg.draw)

        if event == "-SHOW_SECOND-":
            set_visible(final, values[event], fig_agg.draw)

        if event == "-SHOW_POINTS-":
            set_visible(scatter_points, values[event], fig_agg.draw)

        if event == "-SHOW_CURRENT-":
            set_visible(cur_point, values[event], fig_agg.draw)

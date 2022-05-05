from classes.coordinate import Coordinate
from classes.sample import Sample
from classes.microscope_mover import MicroscopeMover
from gui.gui import GUI
from gui.plot_gui import PlotGUI
from classes.scanner import Scanner
import gui.buttons as buttons
from matplotlib.patches import Rectangle as Rectangle_
import PySimpleGUI as sg

if __name__ == "__main__":
    window = GUI().window
    plot_gui = PlotGUI()
    plot_window = plot_gui.window

    while True:
        window, event, values = sg.read_all_windows()
        if event == sg.WIN_CLOSED:  # if user closes window or clicks cancel
            break

        if event == "-REFRESHCOMPORTS-":
            window["-COM_PORT_CHOOSER-"].Update(values=buttons.get_available_com_ports())

        if event == "-CONNECT-":
            mover = MicroscopeMover(buttons.get_com_port_from_desc(values["-COM_PORT_CHOOSER-"]))

        if "-S1READ_" in event:
            # todo add error pop-up
            try:
                new_values = mover.get_coordinates()
                buttons.update_coordinate_inputs(window[f"-S1CORNER{event[-1]}_X-"], window[f"-S1CORNER{event[-1]}_Y-"],
                                                 new_values)
            except NameError:
                print("Microscope is not connected!")

        if event == "-STEP1SUBMIT-":
            # todo add error handling
            initial_sample = Sample(*[Coordinate(int(values[f"-S1CORNER{i}_X-"]), int(values[f"-S1CORNER{i}_Y-"])) for i in range(1, 5)])
            plot_gui.ax.plot(*initial_sample.center.coord_to_tuple())

            plot_gui.ax.set_xlim(-15000, 15000)
            plot_gui.ax.set_ylim(-15000, 15000)

            plot_gui.ax.add_patch(Rectangle_((initial_sample.left_btm_corner.x, initial_sample.left_btm_corner.y),
                                             initial_sample.btm_edge_length,
                                             initial_sample.left_edge_length,
                                             initial_sample.rotation_angle, alpha=0.50))

            plot_gui.fig_agg.draw()
            # plot_gui.random_point.setdata(first_time_sample.left_btm_corner.xfirst_time_sample.y_center_right.y)
            # plot_gui.fig_agg.draw()
            # todo add saving

        if event == "-STEP1LOAD-":
            # todo add loading
            pass

        if "-S2READ_" in event:
            # todo add error pop-up
            try:
                new_values = mover.get_coordinates()
                buttons.update_coordinate_inputs(window[f"-S2CORNER{event[-1]}_X-"], window[f"-S2CORNER{event[-1]}_Y-"],
                                                 new_values)
            except NameError:
                print("Microscope is not connected!")

        if event == "-STEP2SUBMIT-":
            # todo add error handling
            second_time_sample = Sample(
                *[Coordinate(int(values[f"-S2CORNER{i}_X-"]), int(values[f"-S2CORNER{i}_Y-"])) for i in range(1, 5)])
            plot_gui.ax.add_patch(
                Rectangle_((second_time_sample.left_btm_corner.x, second_time_sample.left_btm_corner.y),
                           second_time_sample.btm_edge_length,
                           second_time_sample.left_edge_length,
                           #  first_time_sample.btm_edge_length,
                           #      first_time_sample.left_edge_length,
                           second_time_sample.rotation_angle, alpha=0.7, color='orange'))
            print(second_time_sample.rotation_angle)

            # plot_gui.ax.plot([second_time_sample.y_center_left.x,second_time_sample.y_center_right.x],
            #                   [second_time_sample.y_center_left.y,second_time_sample.y_center_right.y])

            # plot_gui.ax.plot([-9,9],[-4,4])

            # plot_gui.ax.plot([-5,13],[-13,-5])
            # plot_gui.ax.plot([13,5],[-5,13])

            plot_gui.fig_agg.draw()
        if event == "-NUMBER_OF_SCANS-":
            # todo error handling
            try:
                scanning_point_count = int(values["-NUMBER_OF_SCANS-"])
            except ValueError:
                scanning_point_count = 1

        if event == "-SUMBMISCANNO-":
            scanner = Scanner(second_time_sample.get_scanning_points_from_center(scanning_point_count))

            plot_gui.ax.scatter(scanner.list_of_x_coord(), scanner.list_of_y_coord())

            plot_gui.fig_agg.draw()
            scanner.next_scan()
            # mover.set_coordinates(scanner.current_point_coord[1].x,scanner.current_point_coord[1].y)
            window["-SCANNO-"].update(str(scanner.current_point_no + 1))
            window["-CURRENTXY-"].update(str(scanner.current_point_coord))

        if event == "-PREVIOUS-":
            scanner.previous_scan()
            mover.set_coordinates(scanner.current_point_coord[1].x, scanner.current_point_coord[1].y)
            plot_gui.fig_agg.draw()
            window["-SCANNO-"].update(str(scanner.current_point_no + 1))
            window["-CURRENTXY-"].update(str(scanner.current_point_coord))

        if event == "-NEXT-":
            scanner.next_scan()
            mover.set_coordinates(scanner.current_point_coord[1].x, scanner.current_point_coord[1].y)
            window["-SCANNO-"].update(str(scanner.current_point_no + 1))
            window["-CURRENTXY-"].update(str(scanner.current_point_coord))

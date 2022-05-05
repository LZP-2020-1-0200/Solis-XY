from classes.coordinate import Coordinate
from classes.sample import Sample
from classes.microscope_mover import MicroscopeMover
from gui.gui import GUI
from gui.plot_gui import PlotGUI, set_visible
from classes.scanner import Scanner
import gui.buttons as buttons
from matplotlib.patches import Rectangle as Rectangle_
import PySimpleGUI as sg
import csv


if __name__ == "__main__":
    window = GUI().window
    
    plot_gui = PlotGUI()
    plot_window = plot_gui.window
    axes,fig_agg = plot_gui.ax,plot_gui.fig_agg
    scatter_points,cur_point = plot_gui.points, plot_gui.current_point
  

    while True:
        window, event, values = sg.read_all_windows()
        if event == sg.WIN_CLOSED:  # if user closes window or clicks cancel
            break

        if event == "-REFRESHCOMPORTS-":
            window["-COM_PORT_CHOOSER-"].Update(values=buttons.get_available_com_ports())

        if event == "-CONNECT-":
            print(type(buttons.get_com_port_from_desc(values["-COM_PORT_CHOOSER-"])))
            mover = MicroscopeMover(buttons.get_com_port_from_desc(values["-COM_PORT_CHOOSER-"]))

        if "-S1READ_" in event:
            # todo add error pop-up
            new_values = mover.get_coordinates()
            buttons.update_coordinate_inputs(window[f"-S1CORNER{event[-1]}_X-"],
                                             window[f"-S1CORNER{event[-1]}_Y-"],
                                             new_values)
            
        if "-S1GOTOCOORD" in event:
            pass
            

        if event == "-STEP1SUBMIT-":
            try:
                initial_patch.remove()
            except NameError:
                pass
            # todo add error handling
            initial_sample = Sample(*[Coordinate(int(values[f"-S1CORNER{i}_X-"]), int(values[f"-S1CORNER{i}_Y-"])) for i in range(1, 5)])
            # axes.plot(*initial_sample.center.tuple_nm)
            axes.set_xlim(initial_sample.left_btm_corner.x_nm-(initial_sample.left_btm_corner.x_nm/4), 
                          initial_sample.right_top_corner.x_nm+(initial_sample.left_btm_corner.x_nm/4))
            axes.set_ylim(initial_sample.left_btm_corner.y_nm-(initial_sample.left_btm_corner.y_nm/4), 
                          initial_sample.right_top_corner.y_nm+(initial_sample.right_top_corner.y_nm/4))
            
            print(initial_sample.left_btm_corner.tuple_nm, initial_sample.btm_edge_length,initial_sample.left_edge_length)
           
            # initial_patch = axes.add_patch(Rectangle_(initial_sample.left_btm_corner.tuple_nm,
            #                           initial_sample.btm_edge_length,
            #                           initial_sample.left_edge_length,
            #                           initial_sample.rotation_angle, alpha=0.50))
            
            axes.plot(initial_sample.all_x(),initial_sample.all_y())

            fig_agg.draw()

        if event == "-STEP1LOAD-":
            file = sg.popup_get_file("", no_window=1)
            if not file:
                continue
            
            with open(file) as file2:
                csvReader = csv.reader(file2, delimiter=",")
                for i, row in enumerate(csvReader):
                    print(row)
                    buttons.update_coordinate_inputs(window[f"-S1CORNER{i+1}_X-"],
                                                     window[f"-S1CORNER{i+1}_Y-"],
                                                     [row[0], row[1]])

            # todo add loading
     

        if "-S2READ_" in event:
            # todo add error pop-up
            try:
                new_values = mover.get_coordinates()
                buttons.update_coordinate_inputs(window[f"-S2CORNER{event[-1]}_X-"], window[f"-S2CORNER{event[-1]}_Y-"],
                                                 new_values)
            except NameError:
                print("Microscope is not connected!")

        if event == "-STEP2SUBMIT-":
            try:
                final_patch.remove()
            except NameError:
                pass
            # todo add error handling
            final_sample = Sample(
                *[Coordinate(int(values[f"-S2CORNER{i}_X-"]), int(values[f"-S2CORNER{i}_Y-"])) for i in range(1, 5)])
            final_patch = axes.add_patch(Rectangle_(final_sample.left_btm_corner.tuple_nm,
                                                    final_sample.btm_edge_length,
                                                    final_sample.left_edge_length,
                                                    final_sample.rotation_angle, alpha=0.7, color='orange'))

            fig_agg.draw()
        if event == "-NUMBER_OF_SCANS-":
            # todo error handling
            try:
                scanning_point_count = int(values["-NUMBER_OF_SCANS-"])
                scanner = Scanner(final_sample.get_scanning_points_from_center(scanning_point_count))
                scatter_points.set_data(scanner.list_of_x_coord(), scanner.list_of_y_coord())
                fig_agg.draw()
            except ValueError:
                scanning_point_count = 1

        if event == "-SUMBMISCANNO-":
            scanner.next_scan()
            mover.set_coordinates(*scanner.current_point_coord.tuple)
            cur_point.set_data(*scanner.current_point_coord.tuple_nm)
            window["-SCANNO-"].update(str(scanner.current_point_no + 1))
            window["-CURRENTXY-"].update(str(scanner.current_point_coord))

        if event == "-PREVIOUS-" or event == "-NEXT-":
            scanner.previous_scan() if event == "-PREVIOUS-" else scanner.next_scan()
            mover.set_coordinates(*scanner.current_point_coord.tuple)
            cur_point.set_data(*scanner.current_point_coord.tuple_nm)
            fig_agg.draw()
            window["-SCANNO-"].update(str(scanner.current_point_no + 1))
            window["-CURRENTXY-"].update(str(scanner.current_point_coord))
            
            
        #plot gui events
        if event == "-SHOW_FIRST-":
            set_visible(initial_patch,values[event],fig_agg.draw)
            
        if event == "-SHOW_SECOND-":
            set_visible(final_patch,values[event],fig_agg.draw)
             
        if event == "-SHOW_POINTS-":
            set_visible(scatter_points,values[event],fig_agg.draw)
            
        if event == "-SHOW_CURRENT-":
            set_visible(cur_point, values[event],fig_agg.draw)
            


import coloredlogs
import logging
import PySimpleGUI as sg
import csv

from classes.coordinate import Coordinate, get_new_point
from classes.microscope_mover import MicroscopeMover
from classes.scanner import Scanner
from gui.position_gui import PositionGUI, disable_element
import gui.buttons as btn
from gui.helpers import str_to_int

logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO')

def main():
    gui = PositionGUI()
    mover = MicroscopeMover()
    scanner = Scanner()
    window = gui.window
    
    points: dict[str,Coordinate] = {}
    
    while 1:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED:
            break
        
        
        if event == "-REFRESHCOMPORTS-":
            window["-COM_PORT_CHOOSER-"].Update(values=btn.get_available_com_ports())
            
            
        if event == "-CONNECT-":
            port_description = values["-COM_PORT_CHOOSER-"]
            com_port = btn.get_com_port_from_desc(port_description)
            
            if mover.connect(com_port):
                disable_element(window, "-COM_PORT_CHOOSER-")
                disable_element(window, "-REFRESHCOMPORTS-")
                disable_element(window, "-CONNECT-")
                
                
        if "READ_COORD" in event:
            points.pop(f's{event[2]}point{event[-2]}', None)
            point = mover.get_coordinates()

            if not point:
                continue
            
            input_x = window[f"-S{event[2]}CORNER{event[-2]}_X-"]
            input_y = window[f"-S{event[2]}CORNER{event[-2]}_Y-"]
            
            btn.update_coordinate_inputs(input_x, input_y, point)
            logger.info(f"Read point X: {point.x} Y: {point.y}")

                
        if "GOTOCORD" in event:
            go_x = values[f"-S{event[2]}CORNER{event[-2]}_X-"]
            go_y = values[f"-S{event[2]}CORNER{event[-2]}_Y-"]
            
            go_x_int = str_to_int(go_x)
            go_y_int = str_to_int(go_y)
            
            if not go_x_int or not go_y_int:
                continue
            
            go_cord = Coordinate(go_x_int, go_y_int)
            mover.set_coordinates(go_cord)
            
            
        if event == "-STEP1SUBMIT-":
            error_in_validation = False
            
            for i in range(1,3):
                x = values[f"-S1CORNER{i}_X-"]
                y = values[f"-S1CORNER{i}_Y-"]

                x_int = str_to_int(x)
                y_int = str_to_int(y)

                if not x_int or not y_int:
                    error_in_validation = True
                    break

                point_key = f's1point{i}'
                points[point_key] = Coordinate(x_int, y_int)
                
            if error_in_validation:
                continue
                
            save_path = sg.popup_get_file("", no_window=1, default_extension=".txt", save_as=1)
            if not save_path:
                continue
            
            with open(save_path, 'w', newline='') as file:
                writer = csv.writer(file, delimiter=',')
                writer.writerow(points['s1point1'].tuple)
                writer.writerow(points['s1point2'].tuple)
            logger.info(f"Successfully saved points at {save_path}")

               
                
        if event == "-STEP1LOAD-":
            load_path = sg.popup_get_file("", no_window=1, file_types=(("TXT files", "*.txt"),), )
            
            if not load_path:
                continue
            
            with open(load_path) as file:
                csv_reader = csv.reader(file, delimiter=",")
                for i, row in enumerate(csv_reader):
                    # TODO error handling
                    coord = Coordinate(int(row[0]),int(row[1]))
                    points[f's1point{i+1}'] = coord
                    
                    input_x = window[f"-S1CORNER{i + 1}_X-"]
                    input_y = window[f"-S1CORNER{i + 1}_Y-"]
                    
                    btn.update_coordinate_inputs(input_x, input_y, coord)
            logger.info("Successfully loaded initial points")
            
            disable_element(window, '-S1CORNER1_X-')
            disable_element(window, '-S1CORNER1_Y-')
            disable_element(window, '-S1CORNER2_X-')
            disable_element(window, '-S1CORNER2_Y-')
            disable_element(window, '-S1READ_COORD1-')
            disable_element(window, '-S1GOTOCORD1-')
            disable_element(window, '-S1READ_COORD2-')
            disable_element(window, '-S1GOTOCORD2-')
            disable_element(window, '-STEP1SUBMIT-')
            disable_element(window, '-STEP1LOAD-')
            
                
        if event == "-STEP2SUBMIT-":
            
            if 's1point1' not in points or 's1point2' not in points:
                logger.error("One of the initial points is missing")
                continue
            
            if 's2point1' not in points or 's2point2' not in points:
                logger.error("One of the new points is missing")
                continue
            
            # TODO add some kind of error handling
            with open(load_path[:-4] + "recalculated.txt", 'w', newline='') as file:
                writer = csv.writer(file, delimiter=',')
                writer.writerow(points['s2point1'].tuple)
                writer.writerow(points['s2point2'].tuple)
            logger.info(f"Successfully saved points at {load_path}")

            points_load_path = sg.popup_get_file("", no_window=1, file_types=(("TXT files", "*.txt"),), )
            
            if not points_load_path:
                continue
            
            scanner.load_coordinates(points_load_path)
            new_points = []
            
            # TODO check and delete print statements
            old_corner = min(points['s1point1'],points['s1point2'])
            print("old corner: ", old_corner)
            new_corner_btm = min(points['s2point1'],points['s2point2'])
            print("new_corner_btm: ", new_corner_btm)
            new_corner_top = max(points['s2point1'], points['s2point2'])
            print("new corner top: ", new_corner_top)
            
            for old_point in scanner.all_scanner_points:
                new_point = get_new_point(old_point, old_corner, new_corner_btm, new_corner_top)
                new_points.append(new_point)
                print("\nold point: ", old_point)
                print("new_point: ", new_point)
                
            scanner.set_points(new_points)
            scanner.save_coordinate(points_load_path[:-4] + '_recalculated.txt')
            
        # TODO delete
        if event == "-TEST-":
            load_path = sg.popup_get_file("", no_window=1, file_types=(("TXT files", "*.txt"),), )
            
            if not load_path:
                continue
            
            with open(load_path) as file:
                csv_reader = csv.reader(file, delimiter=",")
                for i, row in enumerate(csv_reader):
                    coord = Coordinate(int(row[0]),int(row[1]))
                    points[f's2point{i+1}'] = coord
                    btn.update_coordinate_inputs(window[f"-S2CORNER{i + 1}_X-"],
                                                     window[f"-S2CORNER{i + 1}_Y-"],
                                                     coord)
                logger.info("Successfully loaded initial points")
         
        if event == "-SAMEVALUES-":
            
            if 's1point1' not in points or 's1point2' not in points:
                logger.error("One of the initial points is missing")
                continue
            
            points["s2point1"] = points["s1point1"]
            
            input_x_1 = window["-S2CORNER1_X-"]
            input_y_1 = window["-S2CORNER1_Y-"]
            btn.update_coordinate_inputs(input_x_1, input_y_1, points["s2point1"])
            
            points["s2point2"] = points["s1point2"]
            
            input_x_2 = window["-S2CORNER2_X-"]
            input_y_2 = window["-S2CORNER2_Y-"]
            btn.update_coordinate_inputs(input_x_2, input_y_2, points["s2point2"])

         
if __name__ == "__main__":
    main()
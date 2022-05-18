import coloredlogs
import logging
import PySimpleGUI as sg
import time

from classes.coordinate import Coordinate
from classes.microscope_mover import MicroscopeMover
from classes.sample import get_scanning_points_from_points
from classes.scanner import Scanner
from classes.solis import Automatization
from gui.new_gui import AutomatizationGUI
import gui.buttons as buttons

P_LETTER = ord("p"), ord("P")
S_LETTER = ord("s"), ord("S")


logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO')
coloredlogs.install(level='INFO', logger=logger)

paused = False
stopped = False


def disable(window : sg.Element, key : str):
    window[key].update(disabled = True)

def start_scanning(window : sg.Element, scanner: Scanner, mover: MicroscopeMover, solis: Automatization):
    global paused, stopped
    logger.info("Started scanning sequence")
    solis.connect_to_solis("Process Explorer - *")
    for i, point in enumerate(scanner.all_scanner_points):
        window["-SCANNO-"].update(scanner.current_point_no + 1)
        window["-CURRENTXY-"].update(scanner.current_point_coord)
        scanner.next_scan()
        mover.set_coordinates(point)
        for j in range(3):
            while paused:
                time.sleep(0.5)
            if stopped:
                return
            solis.capture_and_save(f"Point nr. {i+1}. {point.tuple}_{j+1}", i == 0 and j == 0)


def main():
    gui = AutomatizationGUI()
    mover = MicroscopeMover()
    scanner = Scanner()
    solis = Automatization()
    window = gui.window
    
    
    points_of_interest = []
    
    global paused, stopped
    
    while 1:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        
        if event == "-REFRESHCOMPORTS-":
            window["-COM_PORT_CHOOSER-"].Update(values=buttons.get_available_com_ports())
                
        if event == "-CONNECT-":
            if mover.connect(buttons.get_com_port_from_desc(values["-COM_PORT_CHOOSER-"])):
                disable(window, "-COM_PORT_CHOOSER-")
                disable(window, "-REFRESHCOMPORTS-")
                disable(window, "-CONNECT-")
                
        if event == "-SUMBMISCANNO-":
            try:
                numb_of_scans = int(values["-NUMBER_OF_SCANS-"])
            except ValueError:
                logger.error(
                    f"Could not not convert \"{values['-NUMBER_OF_SCANS-']}\" to Integer")
                continue

            if len(points_of_interest) < 2:
                logger.error(
                    f"At least 2 points must be chosen! Current point count: {len(points_of_interest)}")
                continue
            
            i = 0
            all_between_points: list[Coordinate] = []
            while i < len(points_of_interest) - 1:
                between_points = get_scanning_points_from_points(
                    points_of_interest[i], points_of_interest[i + 1], numb_of_scans)
                for point in between_points:
                    all_between_points.append(point)
                i += 1
            
            scanner.set_points(all_between_points)
            logger.info("Points submitted successfully")
            stopped, paused = False, False

            disable(window, "-NUMBER_OF_SCANS-")
            disable(window, "-SUMBMISCANNO-")
                
        
        if event == "-ADDPOINTOFINT-":
            
            point = mover.get_coordinates()
            if point:
                points_of_interest.append(point)
                logger.info(f"Added point nr. {len(points_of_interest)}. with coordinates: {points_of_interest[-1]}")
                
          
        if event == "-REMOVELAST-":
            if len(points_of_interest):
                logger.info(f"Removed point nr. {len(points_of_interest)}. with coordinates: {points_of_interest[-1]}")
                points_of_interest.pop()
            else:
                logger.error("List of points is empty!")
                
        
        if event == "-SAVESCANPOINTS-":
            if not scanner.all_scanner_points:
                logger.error("No points for saving !")
                continue
            points_save_path = sg.popup_get_file("", no_window=1, default_extension=".txt", save_as=1)
            if points_save_path:
                scanner.save_coordinate(points_save_path)
                points_save_path = None
                
        if event == "-LOADSCANPOINTS-":
            points_load_path = sg.popup_get_file("", no_window=1, default_extension=".txt")
            if points_load_path and scanner.load_coordinates(points_load_path):
                points_load_path = None
                disable(window, "-NUMBER_OF_SCANS-")
                disable(window, "-SUMBMISCANNO-")
                disable(window, "-SAVESCANPOINTS-")
                disable(window, "-LOADSCANPOINTS-")
                disable(window, "-ADDPOINTOFINT-")
                disable(window, "-REMOVELAST-")


        if event == "-STARTSCAN-":
            if not scanner.all_scanner_points:
                logger.error("No scanning points loaded or submitted")
                continue
            
            if not mover.port_is_open():
                logger.error("Cannot start scanning: Microscope is not connected")
                continue
            
            window.perform_long_operation(lambda : start_scanning(scanner,mover,solis), "-SCANEND-")
            
        if len(event) == 1 and ord(event) in P_LETTER:
            paused = True if not paused else False
            logger.warning("Paused Scanning" if paused else "Continue scanning")
            
        if len(event) == 1 and ord(event) in S_LETTER:
            stopped = True
            logger.warning("Abort scanning")


if __name__ == "__main__":
    main()

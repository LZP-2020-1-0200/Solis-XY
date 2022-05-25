import coloredlogs
import logging
import PySimpleGUI as sg
import time

from classes.coordinate import Coordinate
from classes.microscope_mover import MicroscopeMover
from classes.scanner import Scanner, get_scanning_points_from_points
from classes.solis import Automatization
from gui.scanner_gui import AutomatizationGUI, disable_element
import gui.buttons as btn
from gui.helpers import get_load_path, str_to_int, get_save_path

PADDING = 7

P_LETTER = ord("p"), ord("P")
S_LETTER = ord("s"), ord("S")


logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO')

paused = False
stopped = False



    
def construct_number_with_padding(number : int):
    number_as_str = str(number)
    digit_count = len(number_as_str)
    return f"{'0'*(PADDING - digit_count)}{number_as_str}"
    

def start_scanning(window : sg.Element, scanner: Scanner, mover: MicroscopeMover, solis: Automatization, scans_per_point : int):
    global paused, stopped
    logger.info("Started scanning sequence")
    for i, point in enumerate(scanner.all_scanner_points):
        point_nr = construct_number_with_padding(i+1)
        window["-SCANNO-"].update(scanner.current_point_no + 1)
        window["-CURRENTXY-"].update(scanner.current_point_coord)
        scanner.next_scan()
        mover.set_coordinates(point)
        for j in range(scans_per_point):
            
            while paused:
                time.sleep(0.5)
            if stopped:
                return
            
            if scans_per_point == 1:
                solis.capture_and_save(f"Point nr. {point_nr}. {point.tuple}", i == 0 and j == 0)
            else:
                solis.capture_and_save(f"Point nr. {point_nr}. {point.tuple}_{j+1}", i == 0 and j == 0)
            
            
    logger.info("Successfully ended scanning sequence")


def main():
    global paused, stopped
    
    solis = Automatization("Andor SOLIS for Spectroscopy: *")
    if not solis.success:
        return
    
    gui = AutomatizationGUI()
    mover = MicroscopeMover()
    scanner = Scanner()
    window = gui.window
    
    points_of_interest = []
    
    while 1:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        
        if event == "-REFRESHCOMPORTS-":
            window["-COM_PORT_CHOOSER-"].Update(values=btn.get_available_com_ports())
                
        if event == "-CONNECT-":
            if mover.connect(btn.get_com_port_from_desc(values["-COM_PORT_CHOOSER-"])):
                disable_element(window, "-COM_PORT_CHOOSER-")
                disable_element(window, "-REFRESHCOMPORTS-")
                disable_element(window, "-CONNECT-")
                
        if event == "-SUMBMISCANNO-":
            
            numb_of_scans = str_to_int(values["-NUMBER_OF_SCANS-"])
            num_of_scans_per_point = str_to_int(values["-NUMOFSCANS-"])
            
            if not numb_of_scans:
                continue
            

            if len(points_of_interest) < 2:
                logger.error(f"At least 2 points must be chosen! Current point count: {len(points_of_interest)}")
                continue
            
            
            if not num_of_scans_per_point:
                continue
            
            
            if numb_of_scans <= 0 or num_of_scans_per_point <= 0:
                logger.error("Negative or zero number of scans")
                continue

            
            i = 0
            all_between_points: list[Coordinate] = []
            while i < len(points_of_interest) - 1:
                between_points = get_scanning_points_from_points(points_of_interest[i], points_of_interest[i + 1], numb_of_scans, num_of_scans_per_point)
                for point in between_points:
                    all_between_points.append(point)
                i += 1
            
            scanner.set_points(all_between_points)
            logger.info("Points submitted successfully")
            stopped, paused = False, False

            disable_element(window, "-NUMBER_OF_SCANS-")
            disable_element(window, "-SUMBMISCANNO-")
            disable_element(window, "-NUMOFSCANS-")
                
        
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
            points_save_path = get_save_path()
            if points_save_path:
                scanner.save_coordinate(points_save_path)
                points_save_path = None
                
        if event == "-LOADSCANPOINTS-":
            points_load_path = get_load_path()
            if points_load_path and scanner.load_coordinates(points_load_path):
                points_load_path = None
                disable_element(window, "-NUMBER_OF_SCANS-")
                disable_element(window, "-SUMBMISCANNO-")
                disable_element(window, "-SAVESCANPOINTS-")
                disable_element(window, "-LOADSCANPOINTS-")
                disable_element(window, "-ADDPOINTOFINT-")
                disable_element(window, "-REMOVELAST-")


        if event == "-STARTSCAN-":
            if not scanner.all_scanner_points:
                logger.error("No scanning points loaded or submitted")
                continue
            
            if not mover.port_is_open():
                logger.error("Cannot start scanning: Microscope is not connected")
                continue
            
            window.perform_long_operation(lambda : start_scanning(window,scanner,mover,solis), "-SCANEND-")
            
        if len(event) == 1 and ord(event) in P_LETTER:
            paused = True if not paused else False
            logger.warning("Paused Scanning" if paused else "Continue scanning")
            
        if len(event) == 1 and ord(event) in S_LETTER:
            stopped = True
            logger.warning("Abort scanning")


if __name__ == "__main__":
    main()

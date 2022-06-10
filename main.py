import PySimpleGUI as sg

import gui.buttons as btn
from classes.logger import Logger
from classes.microscope_mover import mover
from gui.buttons import get_available_com_ports
from gui.helpers import disable_element
from position import main as position_main
from scanner import main as scanner_main
from scanning_points import main as points_main

logger = Logger(__name__).get_logger()


def main():
    layout = [
        [
            sg.T("COM Port: "),
            sg.Combo(
                [*get_available_com_ports()], key="-COM_PORT_CHOOSER-", readonly=True, s=(20, 2), font=("Verdana", "9")
            ),
            sg.B("Refresh", key="-REFRESHCOMPORTS-"),
            sg.B("Connect", key="-CONNECT-"),
        ],
        [
            sg.B("Corners", key="-CONVERTER-", expand_x=True),
            sg.B("Scanning Points", key="-SCANPOINTS-", expand_x=True),
            sg.B("Scanner", key="-SCANNER-", expand_x=True),
        ],
    ]
    window = sg.Window("Solis-XY", layout=layout, finalize=True, font=("Verdana", "12"))

    microscope_connected = False

    while 1:
        event, values = window.read()

        if event == sg.WIN_CLOSED:

            mover.close_connection() if microscope_connected else None
            break

        if event == "-REFRESHCOMPORTS-":
            window["-COM_PORT_CHOOSER-"].Update(values=btn.get_available_com_ports())

        if event == "-CONNECT-":
            port_description: str = values["-COM_PORT_CHOOSER-"]
            com_port = btn.get_com_port_from_desc(port_description)

            microscope_connected = mover.connect(com_port)

            if not microscope_connected:
                continue

            disable_element(window, "-COM_PORT_CHOOSER-")
            disable_element(window, "-REFRESHCOMPORTS-")
            disable_element(window, "-CONNECT-")

        if event == "-SCANNER-":

            if not microscope_connected:
                logger.error("Choose COM port first!")
                continue

            scanner_main()

        if event == "-CONVERTER-":

            if not microscope_connected:
                logger.error("Choose COM port first!")
                continue

            position_main()

        if event == "-SCANPOINTS-":

            if not microscope_connected:
                logger.error("Choose COM port first!")
                continue

            points_main()


if __name__ == "__main__":
    main()

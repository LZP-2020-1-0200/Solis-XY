import PySimpleGUI as sg
import serial.tools.list_ports
from classes.coordinate import Coordinate


def get_available_com_ports() -> list[str]:
    ports = serial.tools.list_ports.comports()
    return [desc for (_, desc, _) in sorted(ports)]


def get_com_port_from_desc(com_port_desc: str):
    if not com_port_desc:
        return

    ports = serial.tools.list_ports.comports()
    for port, desc, _ in ports:
        if com_port_desc in desc:
            return port


def update_coordinate_inputs(input1: sg.Element, input2: sg.Element, coord: Coordinate):
    input1.update(coord.x)
    input2.update(coord.y)

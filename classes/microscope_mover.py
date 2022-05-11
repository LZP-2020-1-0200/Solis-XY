import time

import serial
import serial.tools.list_ports

BAUDRATE = 9600


class MicroscopeMover:

    def __init__(self, com_port):
        # todo Add normal pop-up
        try:
            self.serial = serial.Serial(port=com_port, baudrate=BAUDRATE)
        except:
            print("Could not connect to serial port")

    def get_coordinates(self) -> list[int, int]:
        self.serial.write("P \r".encode())
        coord_string = self.serial.read_until(b'\r').decode().split(',')[:2]
        return int(coord_string[0]), int(coord_string[1])

    def set_coordinates(self, x: int, y: int):

        string = f"G,{x},{y} \r"
        self.serial.write(string.encode())
        while self.serial.read(2) != b"R\r":
            time.sleep(0.05)

    def reset_coordinates(self):
        self.serial.write(b"PS,0,0 \r")
        self.serial.read(2)

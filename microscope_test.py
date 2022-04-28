import time

import serial
import serial.tools.list_ports

BAUDRATE = 9600


class MicroscopeMover:

    def __init__(self, com_port):
        self.serial = serial.Serial(port=com_port, baudrate=BAUDRATE)

    def get_coordinates(self) -> list[int, int]:
        self.serial.write("P \r".encode())
        coord_string = self.serial.read_until(b'\r').decode().split(',')[:2]
        return int(coord_string[0]), int(coord_string[1])*-1
        # return [int(x) for x in coord_string.split(',')[:2]]

    def set_coordinates(self, x: int, y: int):
        string = f"G,{x},{y*-1} \r"
        self.serial.write(string.encode())
        while self.serial.read(2) != b"R\r":
            time.sleep(0.05)

    def reset_coordinates(self):
        self.serial.write(b"PS,0,0 \r")
        self.serial.read(2)


mover = MicroscopeMover("COM6")
print(mover.get_coordinates())
mover.set_coordinates(25000, 25000)
print(mover.get_coordinates())
# ser.write(b"YD,0\r")
# print(ser.read(2))
# reset_coordinates(ser)
# time.sleep(1)
# print(get_coordinates(ser))

# ser.write(b"PS,0,0<CR> \r")
# print(ser.read(2))
# print(get_coordinates(ser))
# set_coordinates(ser,0,0)
# set_coordinates(ser, 9200000, 9200000)
#
# print(get_coordinates(ser))

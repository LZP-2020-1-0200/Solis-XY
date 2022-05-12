import time

import serial
import serial.tools.list_ports

BAUDRATE = 9600


class MicroscopeMover:

    def __init__(self, com_port):
        # todo Add normal pop-up
        try:
            self.serial = serial.Serial(port=com_port, baudrate=BAUDRATE)
            self.set_speed()
        except:
            print("Could not connect to serial port")

    def get_coordinates(self) -> list[int, int]:
        self.serial.write("P \r".encode())
        coord_string = self.serial.read_until(b'\r').decode().split(',')[:2]
        print(coord_string)
        return int(coord_string[0]), int(coord_string[1])

    def set_coordinates(self, x: int, y: int):
        print(f"Going to: {x} {y}")
        string = f"G,{x},{y} \r"
        time_counter = 0
        self.serial.write(string.encode())
        while self.serial.read(2) != b"R\r":
            time.sleep(0.05)
            time_counter + 1
            if time_counter > 150:
                a = self.serial.read(2)
                print(a)
                break

    def reset_coordinates(self):
        self.serial.write(b"PS,0,0 \r")
        self.serial.read(2)

    def set_speed(self, speed: int = 40):
        string = f"SMS,{speed} \r".encode()
        self.serial.write(string)
        while self.serial.read(2) != b"0\r":
            time.sleep(1)

# # test
# hey = MicroscopeMover("COM6")
# hey.set_speed(40)
# string = "SMS,20 \r".encode()
# hey.serial.write(string)
# time.sleep(2)
# print(hey.serial.read(2))

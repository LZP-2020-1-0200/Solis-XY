import coloredlogs
import logging
import time
import serial
import serial.tools.list_ports

from classes.coordinate import Coordinate


logger = logging.getLogger(__name__)
coloredlogs.install(level="INFO")

BAUDRATE = 9600


class MicroscopeMover:
    def __init__(self):
        self.serial: serial.Serial = serial.Serial()

    def connect(self, com_port: str) -> bool:

        if not com_port:
            logger.error("No COM port selected !")
            return False

        try:
            self.serial = serial.Serial(port=com_port, baudrate=BAUDRATE)
            logger.info(f"Successfully connected to {com_port}")

        except Exception as e:
            logger.error(e)
            return False

        self.set_speed()
        return True

    def get_coordinates(self) -> Coordinate | None:
        if not self.port_is_open():
            logger.error("Microscope is not connected!")
            return

        self.serial.write("P \r".encode())
        coord_string = self.serial.read_until(b"\r").decode().split(",")[:2]
        cord = Coordinate(int(coord_string[0]), int(coord_string[1]))
        logger.info(f"Read point {cord}")
        return cord

    def set_coordinates(self, cord: Coordinate):
        if not self.port_is_open():
            logger.error("Microscope is not connected!")
            return

        logger.info(f"Going to: {cord.x} {cord.y}")
        string = f"G,{cord.x},{cord.y} \r"
        time_counter = 0
        self.serial.write(string.encode())

        while self.serial.read(2) != b"R\r":
            time.sleep(0.05)
            time_counter = +1
            if time_counter > 600:
                self.serial.read(2)
                break

        time.sleep(0.5)

    def reset_coordinates(self):
        if not self.port_is_open():
            logger.error("Microscope is not connected!")
            return

        self.serial.write(b"PS,0,0 \r")
        self.serial.read(2)

    def set_speed(self, speed: int = 40):
        if not self.port_is_open():
            logger.error("Microscope is not connected!")
            return
        string = f"SMS,{speed} \r".encode()
        self.serial.write(string)

        while self.serial.read(2) != b"0\r":
            time.sleep(0.05)

        logger.info(f"Set speed to {speed}%")

    def close_connection(self):
        if not self.port_is_open():
            logger.error("Microscope is not connected!")
            return

        self.serial.close()
        logger.info("Closed connection")

    def port_is_open(self) -> bool:
        if not self.serial:
            return False
        return self.serial.isOpen()

import coloredlogs
import logging
import csv

from classes.coordinate import Coordinate


logger = logging.getLogger(__name__)
coloredlogs.install(level="INFO")


def get_scanning_points(pnt1: Coordinate, pnt2: Coordinate, num_points: int) -> list[Coordinate]:
    spacing = (pnt2 - pnt1) / (num_points + 1)
    all_points = [pnt1 + spacing * i for i in range(1, num_points + 1)]
    all_points.append(pnt2)
    return all_points


class Scanner:
    def __init__(self):
        self.all_scanner_points: list[Coordinate] = []
        self.all_point_count = 0
        self.current_point_no = -1
        self.current_point_coord = Coordinate(0, 0)

    def set_points(self, all_points: list[Coordinate]):
        self.all_scanner_points = all_points
        self.all_point_count = len(self.all_scanner_points)

    def previous_scan(self):
        if self.current_point_no <= 0:
            logger.error("There is no previous scan")
            return
        self.current_point_no -= 1
        self.current_point_coord = self.all_scanner_points[self.current_point_no]
        logger.info(f"Current point nr.: {self.current_point_no+1} Coordinates: {self.current_point_coord}")
        return self.current_point_no, self.current_point_coord

    def next_scan(self):
        if self.current_point_no >= self.all_point_count - 1:
            logger.error("There is no next scan")
            return
        self.current_point_no += 1
        self.current_point_coord = self.all_scanner_points[self.current_point_no]
        logger.info(f"Current point nr.: {self.current_point_no+1} Coordinates: {self.current_point_coord}")
        return self.current_point_no, self.current_point_coord

    def save_coordinate(self, path):
        with open(path, "w", newline="") as file:
            csv_writer = csv.writer(file, delimiter=",")
            for point in self.all_scanner_points:
                csv_writer.writerow(list(point.tuple))
        logger.info(f"Successfully saved points at {path}")

    def load_coordinates(self, path):
        self.all_scanner_points = []
        with open(path) as file2:
            csv_reader = csv.reader(file2, delimiter=",")
            for i, row in enumerate(csv_reader):
                if len(row) > 2:
                    logger.error(f"Wrong file, more than 2 columns detected ! ({len(row)}) ")
                    return False
                try:
                    x = int(row[0])
                    y = int(row[1])
                except ValueError as e:
                    logger.error(f"Could not convert{e.args[0].split(':')[-1]} at line: {i+1} to Integer")
                    return False
                self.all_scanner_points.append(Coordinate(x, y))
            self.all_point_count = len(self.all_scanner_points)
            logger.info(f"Successfully loaded points")
            return True

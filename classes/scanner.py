import coloredlogs
import logging

from classes.coordinate import Coordinate, read_all_points_from_file, save_all_points_to_file


logger = logging.getLogger(__name__)
coloredlogs.install(level="INFO")


def get_scanning_points(pnt1: Coordinate, pnt2: Coordinate, num_points: int) -> list[Coordinate]:
    difference = pnt2 - pnt1
    if num_points > 1:
        spacing = Coordinate(difference.x / (num_points - 1), difference.y / (num_points - 1), rounding=False)
    else:
        spacing = Coordinate(0, 0)
    all_points = [pnt1 + spacing * i for i in range(num_points - 1)]
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
        save_all_points_to_file(self.all_scanner_points, path)

    def load_coordinates(self, path):
        self.all_scanner_points = []
        coordinates = read_all_points_from_file(path)

        if not coordinates:
            return False

        self.all_scanner_points = coordinates
        self.all_point_count = len(coordinates)
        return True

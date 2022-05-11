import csv

from classes.coordinate import Coordinate

class Scanner:

    def __init__(self, all_points):
        self.all_scanner_points = all_points
        self.all_point_count = len(self.all_scanner_points)
        self.current_point_no = -1
        self.current_point_coord = Coordinate(0, 0)

    def previous_scan(self):
        if self.current_point_no <= 0:
            return
        self.current_point_no -= 1
        self.current_point_coord = self.all_scanner_points[self.current_point_no]
        return self.current_point_no, self.current_point_coord

    def next_scan(self):
        if self.current_point_no >= self.all_point_count - 1:
            return
        self.current_point_no += 1
        self.current_point_coord = self.all_scanner_points[self.current_point_no]
        return self.current_point_no, self.current_point_coord

    def list_of_x_coord(self):
        return [x.x_nm for x in self.all_scanner_points]

    def list_of_y_coord(self):
        return [y.y_nm for y in self.all_scanner_points]

    def save_coordinate(self, path):
        print(path)
        with open(path, "w", newline='') as file:
            csvReader = csv.writer(file, delimiter=",")
            for point in self.all_scanner_points:
                csvReader.writerow(list(point.tuple))

    def load_coordinates(self, path):
        with open(path) as file2:
            csvReader = csv.reader(file2, delimiter=",")
            for i, row in enumerate(csvReader):
                self.all_scanner_points.append(Coordinate(float(row[0]),float(row[1])))
                # print(row)
                # buttons.update_coordinate_inputs(window[f"-S1CORNER{i + 1}_X-"],
                #                                  window[f"-S1CORNER{i + 1}_Y-"],
                #                                  [row[0], row[1]])


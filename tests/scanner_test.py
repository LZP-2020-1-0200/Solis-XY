import unittest

from classes.coordinate import Coordinate
from classes.scanner import get_scanning_points


class ScanningPointsTest(unittest.TestCase):
    def test_len_of_points(self):
        point_count = 200
        end = Coordinate(65014, -7899)
        start = Coordinate(58916, -7899)
        points = get_scanning_points(start, end, point_count)

        self.assertEqual(point_count, len(points))

    def test_first_point(self):
        point_count = 200
        end = Coordinate(65014, -7899)
        start = Coordinate(58916, -7899)
        points = get_scanning_points(start, end, point_count)

        self.assertEqual(start, points[0])

    def test_last_point(self):
        point_count = 200
        end = Coordinate(65014, -7899)
        start = Coordinate(58916, -7899)
        points = get_scanning_points(start, end, point_count)

        self.assertEqual(end, points[-1])


if __name__ == "__main__":
    unittest.main()

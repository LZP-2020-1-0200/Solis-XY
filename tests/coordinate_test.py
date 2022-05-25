import unittest
from classes.coordinate import *


class CoordinateTopBtmTest(unittest.TestCase):
    def test_top_corner(self):
        cord1 = Coordinate(534, 876)
        cord2 = Coordinate(623, -8764)

        result = max(cord1, cord2)
        self.assertEqual(result, cord1)

    def test_btm_corner(self):
        cord1 = Coordinate(534, 876)
        cord2 = Coordinate(623, -8764)

        result = min(cord1, cord2)
        self.assertEqual(result, cord2)

    def test_read_coordinates(self):
        coordinates = read_all_points_from_file(r"C:\Users\Vladislavs\Desktop\SOLIS-XY data\new_test\points.txt")
        result = coordinates[0]
        real = Coordinate(1000, 1000)

        self.assertEqual(result, real)

    def test_read_coordinates_wrong_file(self):
        coordinates = read_all_points_from_file(r"C:\Users\Vladislavs\Desktop\SOLIS-XY data\new_test\wrong_file.txt")
        self.assertFalse(coordinates)


if __name__ == "__main__":
    unittest.main()

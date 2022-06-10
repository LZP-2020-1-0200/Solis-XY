import unittest

from classes.coordinate import *


class CoordinateTest(unittest.TestCase):
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

    def test_save_coords(self):
        path = r"C:\Users\Vladislavs\Desktop\SOLIS-XY data\new_test\testing_Save2.txt"
        all_cords: list[Coordinate] = []

        for i in range(100000):
            cord = Coordinate(i, i)
            all_cords.append(cord)

        save_all_points_to_file(all_cords, path)
        resulting = read_all_points_from_file(path)[-1]

        self.assertEqual(Coordinate(100000 - 1, 100000 - 1), resulting)


if __name__ == "__main__":
    unittest.main()

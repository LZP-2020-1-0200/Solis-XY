import unittest
from classes.coordinate import Coordinate, get_rotation, rotate_point, get_translation, get_new_point


class RotationTest(unittest.TestCase):

    def test_rotate_point_0(self):
        cord1, cord2 = Coordinate(2, 2), Coordinate(2, 7)
        self.assertEqual(get_rotation(cord1, cord2), 0)

    def test_get_rotation_at_7_deg(self):
        cord1 = Coordinate(870.6768, 1114.42)
        cord2 = Coordinate(-226.147, 10047.3)
        calculated_rotation = get_rotation(cord1, cord2)
        self.assertAlmostEqual(calculated_rotation, 7, places=2)

    def test_calculate_translation_x(self):
        old_cord = Coordinate(2, 2)
        new_cord = Coordinate(1, 2)
        translation = get_translation(old_cord, new_cord)
        calculated_new_cord = old_cord + translation
        self.assertEqual(new_cord, calculated_new_cord)

    def test_calculate_translation_y(self):
        old_cord = Coordinate(2, 2)
        new_cord = Coordinate(2, 1)
        translation = get_translation(old_cord, new_cord)
        calculated_new_cord = old_cord + translation
        self.assertEqual(new_cord, calculated_new_cord)

    def test_calculate_translation_x_y(self):
        old_cord = Coordinate(2, 2)
        new_cord = Coordinate(1, 1)
        translation = get_translation(old_cord, new_cord)
        calculated_new_cord = old_cord + translation
        self.assertEqual(new_cord, calculated_new_cord)

    def test_calculate_translation_x_with_7_deg(self):
        real_translation = Coordinate(-55, 0)
        old_cord = Coordinate(1000, 1000)
        new_cord = Coordinate(815.677, 1114.42)
        calculated_translation = get_translation(old_cord, new_cord, 7)
        self.assertEqual(calculated_translation, real_translation)

    def test_calculate_translation_y_with_7_deg(self):
        real_translation = Coordinate(0, -55)
        old_cord = Coordinate(1000, 1000)
        new_cord = Coordinate(870.677, 1059.42)
        calculated_translation = get_translation(old_cord, new_cord, 7)
        self.assertEqual(calculated_translation, real_translation)

    def test_calculate_translation_xy_with_7_deg(self):
        real_translation = Coordinate(-55, -55)
        old_cord = Coordinate(1000, 1000)
        new_cord = Coordinate(815.677, 1059.42)
        calculated_translation = get_translation(old_cord, new_cord, 7)
        self.assertEqual(calculated_translation, real_translation)

    def test_calculate_new_point_at_7_deg_first(self):
        cord = Coordinate(1000, 1000)
        true_result_coordinate = Coordinate(870.6768, 1114.42)
        calculated_result_coordinate = rotate_point(cord, 7)
        self.assertEqual(calculated_result_coordinate, true_result_coordinate)

    def test_calculate_new_point_at_7_deg_second(self):
        cord = Coordinate(1000, 10000)
        true_result_coordinate = Coordinate(-226.147, 10047.3)
        calculated_result_coordinate = rotate_point(cord, 7)
        self.assertEqual(calculated_result_coordinate, true_result_coordinate)

    def test_get_new_point_of_interest_by_new_corner_btm(self):
        real_old_point = Coordinate(1000, 5000)
        real_new_point = Coordinate(328.2, 5029.6)

        old_corner_btm = Coordinate(1000, 1000)

        new_corner1 = Coordinate(815.677, 1059.42)
        new_corner2 = Coordinate(-281.147, 9992.33)

        final_new_point = get_new_point(real_old_point, old_corner_btm, new_corner1, new_corner2)

        self.assertEqual(real_new_point, final_new_point)

    def test_get_new_point_of_interest_by_new_corner_top(self):
        real_old_point = Coordinate(1000, 5000)
        real_new_point = Coordinate(328.2, 5029.6)

        old_corner_top = Coordinate(1000, 10000)

        new_corner1 = Coordinate(815.677, 1059.42)
        new_corner2 = Coordinate(-281.147, 9992.33)

        final_new_point = get_new_point(real_old_point, old_corner_top, new_corner1, new_corner2, btm=False)

        self.assertEqual(real_new_point, final_new_point)


if __name__ == '__main__':
    unittest.main()

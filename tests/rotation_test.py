import unittest

from classes.coordinate import Coordinate, get_rotation, rotate_point, get_translation, get_new_points


class RotationTest(unittest.TestCase):
    def test_rotation_45(self):
        cord1, cord2 = Coordinate(0, 0), Coordinate(7, 7)
        rotation = get_rotation(cord1, cord2)
        self.assertEqual(rotation, 45)

    def test_rotate_point_90(self):
        cord1, cord2 = Coordinate(2, 2), Coordinate(2, 7)
        self.assertEqual(get_rotation(cord1, cord2), 90)

    def test_get_rotation_at_97_deg(self):
        cord1 = Coordinate(870.6768, 1114.42)
        cord2 = Coordinate(-226.147, 10047.3)
        calculated_rotation = get_rotation(cord1, cord2)
        self.assertAlmostEqual(calculated_rotation, 97, places=2)

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
        self.assertEqual(calculated_translation, real_translation, f"{calculated_translation} != {real_translation}")

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
        real_old_point = [Coordinate(1000, 5000)]
        real_new_point = Coordinate(328.2, 5029.6)

        old_corner_btm = Coordinate(1000, 1000)
        old_corner_top = Coordinate(1000, 10000)
        old_corners = sorted([old_corner_top, old_corner_btm])

        new_corner1 = Coordinate(815.677, 1059.42)
        new_corner2 = Coordinate(-281.147, 9992.33)
        new_corners = sorted([new_corner2, new_corner1])

        final_new_point = get_new_points(real_old_point, old_corners, new_corners)[0]

        self.assertEqual(real_new_point, final_new_point, f"{final_new_point} != {real_new_point}")

    def test_1_real_sample(self):
        old_corner1 = Coordinate(56484, -8726)
        old_corner2 = Coordinate(58988, -13035)
        old_corners = sorted([old_corner1, old_corner2])

        new_corner1 = Coordinate(67374, -7846)
        new_croner2 = Coordinate(67886, -12821)
        new_corners = sorted([new_corner1, new_croner2])

        old_point = Coordinate(55009, -14195)
        real_new_point = Coordinate(63805, -12221)

        calculated_new_point = get_new_points([old_point], old_corners, new_corners)[0]

        difference = abs(real_new_point - calculated_new_point)

        self.assertTrue(difference.x <= 30 and difference.y <= 30)

    def test_2_real_sample(self):
        old_corner1 = Coordinate(63068, -7370)
        old_corner2 = Coordinate(63427, -12358)
        old_corners = sorted([old_corner1, old_corner2])

        new_corner1 = Coordinate(74286, -10417)
        new_croner2 = Coordinate(72975, -15249)
        new_corners = sorted([new_corner1, new_croner2])

        old_point = Coordinate(62285, -10424)
        real_new_point = Coordinate(73016, -13197)

        calculated_new_point = get_new_points([old_point], old_corners, new_corners)[0]

        difference = abs(real_new_point - calculated_new_point)

        self.assertTrue(difference.x <= 500 and difference.y <= 500, f"{difference.tuple}")

    def test_3_real_sample(self):
        old_corner1 = Coordinate(63196, -10611)
        old_corner2 = Coordinate(63053, -15688)
        old_corners = sorted([old_corner1, old_corner2])

        new_corner1 = Coordinate(55153, -8040)
        new_croner2 = Coordinate(56023, -13038)
        new_corners = sorted([new_corner1, new_croner2])

        old_point = Coordinate(60114, -12558)
        real_new_point = Coordinate(52516, -10559)

        calculated_new_point = get_new_points([old_point], old_corners, new_corners)[0]

        difference = abs(real_new_point - calculated_new_point)

        self.assertTrue(difference.x <= 30 and difference.y <= 30)

    def test_4_real_sample(self):
        old_corner1 = Coordinate(55137, -8072)
        old_corner2 = Coordinate(56018, -13005)
        old_corners = sorted([old_corner1, old_corner2])

        new_corner1 = Coordinate(52024, -7721)
        new_croner2 = Coordinate(53453, -12520)
        new_corners = sorted([new_corner1, new_croner2])

        old_point = Coordinate(55654, -9220)
        real_new_point = Coordinate(52669, -8800)

        calculated_new_point = get_new_points([old_point], old_corners, new_corners)[0]

        difference = abs(real_new_point - calculated_new_point)

        self.assertTrue(difference.x <= 30 and difference.y <= 30)

    def test_5_real_sample_left_side(self):
        old_corner1 = Coordinate(47217, -9914)
        old_corner2 = Coordinate(48625, -14673)
        old_corners = sorted([old_corner1, old_corner2])

        new_corner1 = Coordinate(66647, -10310)
        new_croner2 = Coordinate(66350, -15280)
        new_corners = sorted([new_corner1, new_croner2])

        old_point = Coordinate(50545, -14112)
        real_new_point = Coordinate(68357, -15396)

        calculated_new_point = get_new_points([old_point], old_corners, new_corners)[0]

        difference = abs(real_new_point - calculated_new_point)

        self.assertTrue(difference.x <= 30 and difference.y <= 30)

    def test_5_real_sample_right_side(self):
        old_corner1 = Coordinate(53417, -13269)
        old_corner2 = Coordinate(51999, -8484)
        old_corners = sorted([old_corner1, old_corner2])

        new_corner1 = Coordinate(71634, -10589)
        new_croner2 = Coordinate(71347, -15584)
        new_corners = sorted([new_corner1, new_croner2])

        old_point = Coordinate(50545, -14112)
        real_new_point = Coordinate(68357, -15396)

        calculated_new_point = get_new_points([old_point], old_corners, new_corners)[0]

        difference = abs(real_new_point - calculated_new_point)

        self.assertTrue(difference.x <= 30 and difference.y <= 30)

    def test_6_real_sample(self):
        old_corner1 = Coordinate(54666, -8158)
        old_corner2 = Coordinate(55619, -13062)
        old_corners = sorted([old_corner1, old_corner2])

        new_corner1 = Coordinate(66560, -8848)
        new_croner2 = Coordinate(65183, -13660)
        new_corners = sorted([new_corner1, new_croner2])

        old_point = Coordinate(56602, -12861)
        real_new_point = Coordinate(66140, -13941)

        calculated_new_point = get_new_points([old_point], old_corners, new_corners)[0]

        difference = abs(real_new_point - calculated_new_point)

        self.assertTrue(difference.x <= 30 and difference.y <= 30)

    def test_7_real_sample_left(self):
        old_corner1 = Coordinate(65188, -13662)
        old_corner2 = Coordinate(66565, -8852)
        old_corners = sorted([old_corner1, old_corner2])

        new_corner1 = Coordinate(54830, -8064)
        new_croner2 = Coordinate(55050, -13064)
        new_corners = sorted([new_corner1, new_croner2])

        old_point = Coordinate(69448, -9696)
        real_new_point = Coordinate(57836, -7947)

        calculated_new_point = get_new_points([old_point], old_corners, new_corners)[0]

        difference = abs(real_new_point - calculated_new_point)

        self.assertTrue(difference.x <= 30 and difference.y <= 30)

    def test_7_real_sample_right(self):
        old_corner1 = Coordinate(71373, -10256)
        old_corner2 = Coordinate(69990, -15034)
        old_corners = sorted([old_corner1, old_corner2])

        new_corner1 = Coordinate(59827, -7875)
        new_croner2 = Coordinate(60037, -12850)
        new_corners = sorted([new_corner1, new_croner2])

        old_point = Coordinate(69448, -9696)
        real_new_point = Coordinate(57836, -7947)

        calculated_new_point = get_new_points([old_point], old_corners, new_corners)[0]

        difference = abs(real_new_point - calculated_new_point)

        self.assertTrue(difference.x <= 30 and difference.y <= 30)

    def test_7_real_sample_diagonal_btm_top(self):
        old_corner1 = Coordinate(65188, -13662)
        old_corner2 = Coordinate(71373, -10256)
        old_corners = sorted([old_corner1, old_corner2])

        new_corner1 = Coordinate(55050, -13064)
        new_croner2 = Coordinate(59827, -7875)
        new_corners = sorted([new_corner1, new_croner2])

        old_point = Coordinate(69448, -9696)
        real_new_point = Coordinate(57836, -7947)

        calculated_new_point = get_new_points([old_point], old_corners, new_corners)[0]

        difference = abs(real_new_point - calculated_new_point)

        self.assertTrue(difference.x <= 30 and difference.y <= 30)

    def test_7_real_sample_diagonal_top_btm(self):
        old_corner1 = Coordinate(66565, -8852)
        old_corner2 = Coordinate(69990, -15034)
        old_corners = sorted([old_corner1, old_corner2])

        new_corner1 = Coordinate(54830, -8064)
        new_croner2 = Coordinate(60037, -12850)
        new_corners = sorted([new_corner1, new_croner2])

        old_point = Coordinate(69448, -9696)
        real_new_point = Coordinate(57836, -7947)

        calculated_new_point = get_new_points([old_point], old_corners, new_corners)[0]

        difference = abs(real_new_point - calculated_new_point)

        self.assertTrue(difference.x <= 30 and difference.y <= 30)


if __name__ == "__main__":
    unittest.main()

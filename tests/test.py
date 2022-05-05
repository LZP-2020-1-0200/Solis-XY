import unittest
from not_gui import find_corners


class StepOneCornerAllocationCase1(unittest.TestCase):
    all_corners = [(16, 1), (9, 5), (16, 5), (9, 1)]
    btm_left, top_left, btm_right, top_right = find_corners(all_corners)

    def test_btm_left_corner(self):
        self.assertEqual(StepOneCornerAllocationCase1.btm_left, (9, 1))

    def test_top_left_corner(self):
        self.assertEqual(StepOneCornerAllocationCase1.top_left, (9, 5))
        
    def test_btm_right_corner(self):
        self.assertEqual(StepOneCornerAllocationCase1.btm_right, (16, 1))

    def test_top_right_corner(self):
        self.assertEqual(StepOneCornerAllocationCase1.top_right, (16, 5))




class StepOneCornerAllocationCase2(unittest.TestCase):

    def test_btm_left_corner(self):
        all_corners = [(16, 4), (5, 9), (15, 10), (4, 3)]
        btm_left, top_left, btm_right, top_right = find_corners(all_corners)
        self.assertEqual(btm_left, (4, 3))

    def test_top_left_corner(self):
        all_corners = [(16, 4), (5, 9), (15, 10), (4, 3)]
        btm_left, top_left, btm_right, top_right = find_corners(all_corners)
        self.assertEqual(top_left, (5, 9))

    def test_top_right_corner(self):
        all_corners = [(16, 4), (5, 9), (15, 10), (4, 3)]
        btm_left, top_left, btm_right, top_right = find_corners(all_corners)
        self.assertEqual(top_right, (15, 10))

    def test_btm_right_corner(self):
        all_corners = [(16, 4), (5, 9), (15, 10), (4, 3)]
        btm_left, top_left, btm_right, top_right = find_corners(all_corners)
        self.assertEqual(btm_right, (16, 4))


class StepOneCornerAllocationCase2(unittest.TestCase):

    def test_btm_left_corner(self):
        all_corners = [(3,4),(3,2),(1,2),(1,4)]
        btm_left, top_left, btm_right, top_right = find_corners(all_corners)
        self.assertEqual(btm_left, (1,2))

    def test_top_left_corner(self):
        all_corners = [(3,4),(3,2),(1,2),(1,4)]
        btm_left, top_left, btm_right, top_right = find_corners(all_corners)
        self.assertEqual(top_left, (1,4))

    def test_top_right_corner(self):
        all_corners = [(3,4),(3,2),(1,2),(1,4)]
        btm_left, top_left, btm_right, top_right = find_corners(all_corners)
        self.assertEqual(top_right, (3,4))

    def test_btm_right_corner(self):
        all_corners = [(3,4),(3,2),(1,2),(1,4)]
        btm_left, top_left, btm_right, top_right = find_corners(all_corners)
        self.assertEqual(btm_right, (3,2))

if __name__ == '__main__':
    unittest.main()

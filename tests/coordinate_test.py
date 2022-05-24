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


if __name__ == '__main__':
    unittest.main()

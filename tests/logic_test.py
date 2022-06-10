import unittest

from scanner import construct_number_with_padding


class LogicTest(unittest.TestCase):
    def test_construct_filename_9(self):
        self.assertEqual(construct_number_with_padding(9, 1), "P0009x0001")

    def test_construct_filename_99(self):
        self.assertEqual(construct_number_with_padding(99, 5), "P0099x0005")

    def test_construct_filename_999(self):
        self.assertEqual(construct_number_with_padding(999, 421), "P0999x0421")

    def test_construct_filename_9999(self):
        self.assertEqual(construct_number_with_padding(9999, 9999), "P9999x9999")


if __name__ == "__main__":
    unittest.main()

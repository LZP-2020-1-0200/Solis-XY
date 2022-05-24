import unittest
from scanner import construct_number_with_padding


class LogicTest(unittest.TestCase):
    
    
    def test_construct_filename_9(self):
        self.assertEqual(construct_number_with_padding(9), "0000009")
        
    def test_construct_filename_99(self):
        self.assertEqual(construct_number_with_padding(99), "0000099")
        
    def test_construct_filename_999(self):
        self.assertEqual(construct_number_with_padding(999), "0000999")
        
    def test_construct_filename_9999(self):
        self.assertEqual(construct_number_with_padding(9999), "0009999")
        
    def test_construct_filename_99999(self):
        self.assertEqual(construct_number_with_padding(99999), "0099999")
        
    def test_construct_filename_999999(self):
        self.assertEqual(construct_number_with_padding(999999), "0999999")
        
    def test_construct_filename_9999999(self):
        self.assertEqual(construct_number_with_padding(9999999), "9999999")


if __name__ == '__main__':
    unittest.main()

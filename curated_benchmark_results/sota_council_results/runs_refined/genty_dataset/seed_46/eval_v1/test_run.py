import unittest
from genty import genty, genty_dataset

@genty
class TestGentyDataset(unittest.TestCase):
    @genty_dataset(
        ('a', 'b', 'c'),
        ('x', 'y', 'z'),
        first=('1', '2', '3'),
        second=('4', '5', '6')
    )
    def test_values(self, a, b, c):
        expected = [
            ('a', 'b', 'c'),
            ('x', 'y', 'z'),
            ('1', '2', '3'),
            ('4', '5', '6')
        ]
        self.assertIn((a, b, c), expected)

import unittest
from collections import OrderedDict
from genty import genty, genty_dataset

@genty
class TestGentyDataset(unittest.TestCase):
    @genty_dataset(first=(1, 2, 3), second=(4, 5, 9))
    def test_sum(self, a, b, c):
        expected = OrderedDict([('first', (1, 2, 3)), ('second', (4, 5, 9))])
        self.assertEqual(self.__class__.test_sum.genty_datasets, expected)

import unittest
from genty import genty, genty_dataset

@genty
class TestGentyDatasetOverride(unittest.TestCase):
    @genty_dataset(dup=(4, 5, 6))
    @genty_dataset(dup=(1, 2, 3))
    def test_override(self, a, b, c):
        # The outer (first) decorator should override the inner one.
        self.assertEqual((a, b, c), (4, 5, 6))

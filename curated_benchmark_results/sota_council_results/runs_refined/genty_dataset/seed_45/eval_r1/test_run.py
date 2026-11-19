import unittest
from genty import genty_dataset

class TestGentyDataset(unittest.TestCase):
    @genty_dataset(1, 2, 3)
    def test_unnamed(self, a, b, c):
        pass

    def test_datasets_attribute(self):
        datasets = self.test_unnamed.genty_datasets
        self.assertIsInstance(datasets, dict)
        expected_key = '1_and_2_and_3'
        self.assertIn(expected_key, datasets)
        self.assertEqual(datasets[expected_key], (1, 2, 3))

import unittest
from genty import genty_dataset

@genty_dataset(1, 2, 3)
def dummy_test(a, b, c):
    """Dummy test function used only to verify genty_dataset attachment."""
    pass

class TestGentyDataset(unittest.TestCase):
    def test_datasets_attribute(self):
        datasets = dummy_test.genty_datasets
        self.assertIsInstance(datasets, dict)
        expected_key = '1_and_2_and_3'
        self.assertIn(expected_key, datasets)
        self.assertEqual(datasets[expected_key], (1, 2, 3))

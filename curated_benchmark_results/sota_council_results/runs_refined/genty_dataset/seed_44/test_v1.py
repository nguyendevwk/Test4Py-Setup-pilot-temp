import unittest
from collections import OrderedDict
from genty import genty, genty_dataset

@genty
class TestGentyDataset(unittest.TestCase):
    @genty_dataset(first=(1, 2, 3), second=(4, 5, 6))
    def test_datasets(self, a, b, c):
        method = getattr(self.__class__, 'test_datasets')
        assert isinstance(method.genty_datasets, OrderedDict)
        assert list(method.genty_datasets.keys()) == ['first', 'second']
        assert method.genty_datasets['first'] == (1, 2, 3)
        assert method.genty_datasets['second'] == (4, 5, 6)
        for key, val in method.genty_datasets.items():
            if val == (a, b, c):
                current_key = key
                break
        else:
            raise AssertionError("No matching dataset for args")
        assert current_key in ('first', 'second')

import pytest
from collections import OrderedDict
from genty.genty_dataset import genty_dataset

def test_genty_dataset_attaches_datasets_and_keys():
    @genty_dataset(('a1', 'b1'), ('c1',), named=('x',), y=('z',))
    def dummy_test(a, b=None):
        pass

    datasets = dummy_test.genty_datasets
    assert isinstance(datasets, OrderedDict)
    # Order: unnamed args first, then keyword args in definition order
    assert list(datasets.keys()) == ['a1_and_b1', 'c1', 'named', 'y']
    assert datasets['a1_and_b1'] == ('a1', 'b1')
    assert datasets['c1'] == ('c1',)
    assert datasets['named'] == ('x',)
    assert datasets['y'] == ('z',)

import pytest
from collections import OrderedDict
from genty.genty_dataset import genty_dataset

def test_genty_dataset_decorator_sets_and_overrides():
    # Outer decorator (first) should override inner on duplicate keys
    @genty_dataset('single', (1, 2), named=('x', 'y'))
    @genty_dataset('single', (3, 4), named=('x', 'z'))
    def dummy(a, b=None):
        pass

    # The function object should be unchanged
    assert dummy.__name__ == 'dummy'

    # genty_datasets attribute must exist and be an OrderedDict
    assert hasattr(dummy, 'genty_datasets')
    datasets = dummy.genty_datasets
    assert isinstance(datasets, OrderedDict)

    # Expected keys: outer unnamed, outer named, inner unnamed
    expected_keys = ['single', '1, 2', 'named']
    assert list(datasets.keys()) == expected_keys

    # Values must match the supplied datasets
    assert datasets['single'] == ('single',)
    assert datasets['1, 2'] == (1, 2)
    assert datasets['named'] == ('x', 'y')

    # Inner duplicate keys are overridden by outer
    assert datasets['named'] == ('x', 'y')
    assert datasets['single'] == ('single',)

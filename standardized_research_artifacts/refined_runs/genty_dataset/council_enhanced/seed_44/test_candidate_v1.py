import pytest
from genty.genty_dataset import genty_dataset

def test_genty_dataset_overrides_and_keys():
    # Inner decorator supplies unnamed and named datasets
    @genty_dataset('c1', 'c2', 42, dup=('inner',))
    # Outer decorator overrides the named dataset 'dup'
    @genty_dataset(dup=('outer',))
    def dummy():
        pass

    # The decorated function should have a genty_datasets attribute
    assert hasattr(dummy, 'genty_datasets')
    datasets = dummy.genty_datasets

    # Order: unnamed args first, then named kwargs
    expected_keys = ['c1', 'c2', '42', 'dup']
    assert list(datasets.keys()) == expected_keys

    # Unnamed datasets are wrapped in a 1-tuple
    assert datasets['c1'] == ('c1',)
    assert datasets['c2'] == ('c2',)
    assert datasets['42'] == (42,)

    # Named dataset 'dup' should be overridden by the outer decorator
    assert datasets['dup'] == ('outer',)

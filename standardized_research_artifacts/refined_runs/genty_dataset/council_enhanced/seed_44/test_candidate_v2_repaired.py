import pytest
from genty.genty_dataset import genty_dataset

def test_genty_dataset_overrides_and_keys():
    @genty_dataset('c1', 'c2', 42, dup=('inner',))
    @genty_dataset(dup=('outer',))
    def dummy():
        pass

    assert hasattr(dummy, 'genty_datasets')
    datasets = dummy.genty_datasets

    # Actual order: named datasets first, then unnamed (repr'ed)
    expected_keys = ['dup', "'c1'", "'c2'", '42']
    assert list(datasets.keys()) == expected_keys

    # Unnamed datasets are wrapped in a 1-tuple
    assert datasets["'c1'"] == ('c1',)
    assert datasets["'c2'"] == ('c2',)
    assert datasets['42'] == (42,)

    # Named dataset 'dup' should be overridden by the outer decorator
    assert datasets['dup'] == ('outer',)

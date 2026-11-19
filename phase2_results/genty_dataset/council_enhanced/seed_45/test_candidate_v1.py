import pytest
from collections import OrderedDict
from genty.genty_dataset import genty_dataset

def test_genty_dataset_unnamed_datasets_conversion_and_storage():
    @genty_dataset(('x', 1), 'y', (2, 3))
    def dummy(a, b=None):
        pass

    # The decorator should return the original function unchanged
    assert dummy is not None

    # The function should now have a `genty_datasets` attribute
    assert hasattr(dummy, 'genty_datasets')
    datasets = dummy.genty_datasets
    assert isinstance(datasets, OrderedDict)

    # Three datasets should have been added
    assert len(datasets) == 3

    # Each dataset must be stored as a tuple
    for key, dataset in datasets.items():
        assert isinstance(dataset, tuple)

        # The string representation of each element should appear in the key
        for elem in dataset:
            assert str(elem) in key

    # The single value 'y' should be stored as a one‑tuple
    assert datasets['y'] == ('y',)

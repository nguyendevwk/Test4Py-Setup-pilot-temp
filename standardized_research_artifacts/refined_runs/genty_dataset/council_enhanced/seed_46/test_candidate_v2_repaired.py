import pytest
from collections import OrderedDict
from genty.genty_dataset import genty_dataset

def test_genty_dataset_stores_and_overrides_datasets_correctly():
    def dummy(a):  # dummy test method
        pass

    # Apply decorator with unnamed datasets
    dummy = genty_dataset(('a', 1), 'b')(dummy)

    # Verify initial datasets
    assert isinstance(dummy.genty_datasets, OrderedDict)
    assert list(dummy.genty_datasets.keys()) == ["'a', 1", "'b'"]
    assert dummy.genty_datasets["'a', 1"] == ('a', 1)
    assert dummy.genty_datasets["'b'"] == ('b',)

    # Apply decorator with keyword datasets
    dummy = genty_dataset(c=('c',), d=('d', 2))(dummy)

    # Verify order and values after second decorator
    assert list(dummy.genty_datasets.keys()) == ["'a', 1", "'b'", "'c'", "'d'"]
    assert dummy.genty_datasets["'c'"] == ('c',)
    assert dummy.genty_datasets["'d'"] == ('d', 2)

    # Override existing key 'c' with a new dataset
    dummy = genty_dataset(c=('override',))(dummy)

    # Key 'c' should be updated but position unchanged
    assert list(dummy.genty_datasets.keys()) == ["'a', 1", "'b'", "'c'", "'d'"]
    assert dummy.genty_datasets["'c'"] == ('override',)

import pytest
from genty import genty_dataset

def test_genty_dataset_decorator():
    def dummy(a, b, c):
        pass

    dummy = genty_dataset(first=(1, 2, 3), second=(4, 5, 6))(dummy)

    assert hasattr(dummy, "genty_datasets")
    assert list(dummy.genty_datasets.keys()) == ["first", "second"]
    assert dummy.genty_datasets["first"] == (1, 2, 3)
    assert dummy.genty_datasets["second"] == (4, 5, 6)

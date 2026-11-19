import pytest
from genty.genty_dataset import genty_dataset

def test_genty_dataset_decorator_attaches_and_overrides():
    # Inner decorator provides named and unnamed datasets
    @genty_dataset(happy_path=('a1', 'b1'), sad_path=('a2', 'b2'))
    # Outer decorator provides additional unnamed datasets and overrides happy_path
    @genty_dataset('c1', 'c2', happy_path=('x', 'y'))
    def dummy(a, b=None):
        pass

    # The decorated function should have a genty_datasets attribute
    assert hasattr(dummy, "genty_datasets")
    datasets = dummy.genty_datasets

    # Unnamed datasets from the outer decorator become single‑element tuples
    assert datasets["c1"] == ("c1",)
    assert datasets["c2"] == ("c2",)

    # The outer decorator overrides the inner happy_path dataset
    assert datasets["happy_path"] == ("x", "y")
    # The inner sad_path dataset remains unchanged
    assert datasets["sad_path"] == ("a2", "b2")

    # Order: inner keys first, then outer keys appended (outer overrides keep original position)
    expected_order = ["happy_path", "sad_path", "c1", "c2"]
    assert list(datasets.keys()) == expected_order

import pytest
from collections import OrderedDict
from genty.genty_dataset import genty_dataset


def test_genty_dataset_stores_and_overrides_datasets():
    # Base function to decorate
    def dummy_test(a, b):
        pass

    # Apply decorator with unnamed and named datasets
    dummy_test = genty_dataset(
        ('a1', 'b1'),          # unnamed tuple
        'c1',                  # single value
        happy_path=('x', 'y')  # named dataset
    )(dummy_test)

    # Verify that the datasets attribute is an OrderedDict
    assert hasattr(dummy_test, "genty_datasets")
    assert isinstance(dummy_test.genty_datasets, OrderedDict)

    # Unnamed tuple should be stored with key "a1, b1"
    assert dummy_test.genty_datasets["a1, b1"] == ('a1', 'b1')

    # Single value should be stored as a 1‑tuple with key "c1"
    assert dummy_test.genty_datasets["c1"] == ('c1',)

    # Named dataset should use the provided key
    assert dummy_test.genty_datasets["happy_path"] == ('x', 'y')

    # Test that a pre‑existing attribute is preserved and updated
    dummy_test.genty_datasets.update(OrderedDict([("existing", (42,))]))
    dummy_test = genty_dataset(('new',))(dummy_test)
    assert dummy_test.genty_datasets["existing"] == (42,)
    assert dummy_test.genty_datasets["new"] == ('new',)

    # Test that outer decorator overrides inner when keys conflict
    def conflict_test():
        pass

    # Inner decorator (applied first)
    conflict_test = genty_dataset(dup=("inner",))(conflict_test)
    # Outer decorator (applied second)
    conflict_test = genty_dataset(dup=("outer",))(conflict_test)

    # The outer value should override the inner one
    assert conflict_test.genty_datasets["dup"] == ("outer",)

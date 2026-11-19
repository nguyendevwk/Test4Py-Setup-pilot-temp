import sys
import types
import pytest
from collections import OrderedDict

# Provide a minimal stub for the missing `six` dependency
six_stub = types.ModuleType("six")
six_stub.string_types = (str,)
six_stub.iterkeys = lambda d: d.keys()
six_stub.iteritems = lambda d: d.items()
six_stub.itervalues = lambda d: d.values()
six_stub.text_type = str
six_stub.binary_type = bytes
six_stub.PY2 = False
six_stub.PY3 = True
sys.modules["six"] = six_stub

# Now import the target decorator
from genty.genty_dataset import genty_dataset


def test_genty_dataset_decorator_overrides_and_sets():
    # Apply two decorators: the outer one should override the inner on duplicate keys
    @genty_dataset("single", (1, 2), named=("x", "y"))
    @genty_dataset("single", (3, 4), named=("x", "z"))
    def dummy(a, b=None):
        pass

    # Function name should remain unchanged
    assert dummy.__name__ == "dummy"

    # The decorator must attach an OrderedDict named `genty_datasets`
    assert hasattr(dummy, "genty_datasets")
    datasets = dummy.genty_datasets
    assert isinstance(datasets, OrderedDict)

    # The outer decorator should have overridden the inner on duplicate keys
    # The key "single" should map to the outer dataset's args
    assert "single" in datasets
    assert datasets["single"] == (1, 2)

    # The named dataset should also be overridden by the outer decorator
    assert "named" in datasets
    assert datasets["named"] == ("x", "y")

    # The inner unnamed dataset (with args (3, 4)) should not appear
    assert (3, 4) not in datasets.values()

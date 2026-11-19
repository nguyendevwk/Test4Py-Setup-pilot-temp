import pytest
import types
import sys

# Minimal stub for the missing `six` module used by genty
six_stub = types.SimpleNamespace(
    string_types=(str, bytes),
    iteritems=lambda d: d.items(),
    itervalues=lambda d: d.values(),
    iterkeys=lambda d: d.keys(),
    text_type=str,
    binary_type=bytes,
    PY2=False,
    PY3=True,
)
sys.modules["six"] = six_stub

from genty.genty_dataset import genty_dataset


def test_genty_dataset_decorator_behavior():
    @genty_dataset(("a1", "b1"), "c1", named=("x", "y"))
    def dummy(a, b=None):
        pass

    assert hasattr(dummy, "genty_datasets")
    ds = dummy.genty_datasets
    assert list(ds.keys()) == ["a1, b1", "c1", "named"]
    assert ds["a1, b1"] == ("a1", "b1")
    assert ds["c1"] == ("c1",)
    assert ds["named"] == ("x", "y")

    @genty_dataset("dup")
    @genty_dataset("dup", dup=("inner",))
    def dummy2():
        pass

    ds2 = dummy2.genty_datasets
    assert list(ds2.keys()) == ["dup"]
    assert ds2["dup"] == ("dup",)

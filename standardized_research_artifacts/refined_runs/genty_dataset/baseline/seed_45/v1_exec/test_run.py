import pytest
from genty.genty_dataset import genty_dataset


def test_genty_dataset_decorator_behavior():
    # Unnamed arguments: keys are built from string representations of the tuples
    @genty_dataset(('a1', 'b1'), ('c2',))
    def dummy(a, b=None):
        pass

    assert hasattr(dummy, "genty_datasets")
    ds = dummy.genty_datasets
    assert isinstance(ds, type(dummy.genty_datasets))
    # Check that keys contain the expected substrings
    assert any("a1" in k and "b1" in k for k in ds)
    assert any("c2" in k for k in ds)
    # Verify the stored values match the supplied tuples
    values = list(ds.values())
    assert ("a1", "b1") in values
    assert ("c2",) in values

    # Keyword arguments: keys are the supplied names
    @genty_dataset(happy=("x", "y"), sad=("m",))
    def dummy2(a, b=None):
        pass

    assert dummy2.genty_datasets["happy"] == ("x", "y")
    assert dummy2.genty_datasets["sad"] == ("m",)

    # Chaining: outer decorator overrides inner when keys collide
    @genty_dataset(a=("outer",))
    @genty_dataset(a=("inner",))
    def dummy3(a):
        pass

    assert dummy3.genty_datasets["a"] == ("outer",)

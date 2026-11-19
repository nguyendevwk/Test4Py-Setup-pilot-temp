import pytest
from sanic.helpers import Default


def test_default_repr_and_str():
    """Default should have a consistent string representation."""
    d = Default()
    assert repr(d) == "<Default>"
    assert str(d) == "<Default>"
    # repr and str should be identical
    assert repr(d) == str(d)


def test_default_identity_and_comparisons():
    """Each Default instance is unique and not equal to None or object()."""
    d1 = Default()
    d2 = Default()
    # Different instances are not the same object
    assert d1 is not d2
    # Default instances are not equal to None or a generic object
    assert d1 != None
    assert d1 != object()
    # Equality falls back to identity
    assert d1 == d1
    assert d2 == d2


def test_default_in_collections_and_hashability():
    """Default instances can be used as dictionary keys and set members."""
    d = Default()
    # Use as dictionary key
    dct = {d: "value"}
    assert dct[d] == "value"
    # Use in a set
    s = {d}
    assert d in s
    # Adding another Default instance creates a new key
    d2 = Default()
    dct[d2] = "other"
    assert dct[d2] == "other"
    assert len(dct) == 2

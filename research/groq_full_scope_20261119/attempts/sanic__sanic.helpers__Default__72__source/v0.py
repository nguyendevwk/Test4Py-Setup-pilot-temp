import pytest
from sanic.helpers import Default

def test_default_repr_and_str():
    """Default should have a consistent string representation."""
    d = Default()
    assert repr(d) == "<Default>"
    assert str(d) == "<Default>"

def test_default_identity_and_comparison():
    """Each Default instance is unique and not equal to None or other objects."""
    d1 = Default()
    d2 = Default()
    assert d1 is not d2
    assert d1 != d2
    assert d1 != None
    assert d1 != object()

def test_default_in_collection_behavior():
    """Default can be used as a dictionary key and behaves like a unique sentinel."""
    d = Default()
    mapping = {d: "value"}
    assert mapping[d] == "value"
    # Ensure that a different Default instance does not collide
    assert Default() not in mapping

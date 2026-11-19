import pytest
from sanic.helpers import Default

def test_default_repr_and_str():
    """Default should return the same string for __repr__ and __str__."""
    d = Default()
    assert repr(d) == "<Default>"
    assert str(d) == "<Default>"
    # The representation should be stable across multiple calls
    assert repr(d) == repr(d)
    assert str(d) == str(d)

def test_default_is_unique_and_not_none():
    """Default instances should be unique objects and not equal to None."""
    d1 = Default()
    d2 = Default()
    # Each instance is a distinct object
    assert d1 is not d2
    # Neither instance should be equal to None
    assert d1 is not None
    assert d2 is not None
    # They should not be equal to a plain object()
    assert d1 != object()
    assert d2 != object()

def test_default_equality_and_hash_behavior():
    """Default instances should not compare equal to other objects and have a hash."""
    d = Default()
    # Equality with itself is True
    assert d == d
    # Equality with a different type is False
    assert d != 42
    assert d != "Default"
    # Hash should be deterministic and usable in a set
    h = hash(d)
    assert isinstance(h, int)
    s = {d}
    assert d in s

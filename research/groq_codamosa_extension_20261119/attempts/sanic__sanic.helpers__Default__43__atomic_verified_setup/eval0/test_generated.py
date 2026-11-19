import pytest
from sanic.helpers import Default

def test_default_repr_and_str():
    """Default should have a consistent string representation."""
    d = Default()
    assert repr(d) == "<Default>"
    assert str(d) == "<Default>"
    # The representation should not be empty or contain the class name
    assert "<Default>" in repr(d)
    assert "<Default>" not in repr(d).replace("<Default>", "")

def test_default_identity_and_equality():
    """Each Default instance is unique and not equal to another."""
    d1 = Default()
    d2 = Default()
    # Instances are distinct objects
    assert d1 is not d2
    # Equality falls back to identity
    assert d1 != d2
    # A Default instance should not be equal to None or object()
    assert d1 != None
    assert d1 != object()

def test_default_as_sentinel(tmp_path):
    """Default can be used as a sentinel value in functions."""
    sentinel = Default()

    def get_value(value=sentinel):
        # Return the value if it's not the sentinel, otherwise a fallback
        return value if value is not sentinel else "fallback"

    # When no argument is provided, the sentinel triggers the fallback
    assert get_value() == "fallback"

    # When a non-sentinel value is provided, it is returned unchanged
    assert get_value(42) == 42
    assert get_value("hello") == "hello"

    # When the sentinel is explicitly passed, fallback is returned
    assert get_value(sentinel) == "fallback"

    # Ensure that the sentinel is not mistaken for other values
    assert get_value(None) is None
    assert get_value(object()) is not sentinel

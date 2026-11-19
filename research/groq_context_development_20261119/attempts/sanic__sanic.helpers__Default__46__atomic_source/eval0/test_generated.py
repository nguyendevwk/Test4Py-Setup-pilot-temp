import pytest
from sanic.helpers import Default

def test_default_repr_and_str():
    """The Default instance should have a consistent string representation."""
    d = Default()
    assert repr(d) == "<Default>"
    assert str(d) == "<Default>"

def test_default_is_distinct_instances():
    """Each Default instance should be a separate object."""
    d1 = Default()
    d2 = Default()
    assert d1 is not d2
    assert d1 != d2  # default __eq__ falls back to object identity

def test_default_type_and_attributes():
    """The Default class should be a proper class with no unexpected attributes."""
    d = Default()
    assert isinstance(d, Default)
    # Ensure no unexpected attributes are present
    assert set(dir(d)) == set(dir(Default()))
    # The class should not have a __dict__ attribute (since no instance attributes)
    assert not hasattr(d, "__dict__")

import pytest
from sanic.helpers import Default


def test_default_repr_and_str():
    """Default should have a consistent string representation."""
    d = Default()
    assert repr(d) == "<Default>"
    assert str(d) == "<Default>"
    # repr and str should be identical
    assert repr(d) == str(d)


def test_default_identity_and_comparison():
    """Each Default instance is unique and not equal to None or object()."""
    d1 = Default()
    d2 = Default()
    # Different instances are not equal
    assert d1 is not d2
    assert d1 != d2
    # Should not equal None or a generic sentinel
    assert d1 != None
    assert d1 != object()


def test_default_is_not_a_module_and_has_no_attributes():
    """Default should not be mistaken for a module and should not expose attributes."""
    d = Default()
    # ismodule should be False
    from inspect import ismodule
    assert not ismodule(d)
    # Accessing any attribute should raise AttributeError
    with pytest.raises(AttributeError):
        _ = d.some_nonexistent_attribute

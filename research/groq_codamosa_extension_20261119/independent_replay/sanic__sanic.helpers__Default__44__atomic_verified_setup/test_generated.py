import pytest
from sanic.helpers import Default


def test_default_repr_and_str():
    """Default should return the same string for __repr__ and __str__."""
    d = Default()
    rep = repr(d)
    str_rep = str(d)
    assert rep == "<Default>"
    assert str_rep == "<Default>"
    assert isinstance(rep, str)
    assert isinstance(str_rep, str)
    # Ensure that repr and str are identical
    assert rep == str_rep


def test_default_identity_and_equality():
    """Each Default instance is unique and not equal to other objects."""
    d1 = Default()
    d2 = Default()
    assert d1 is not d2  # distinct instances
    # Default has no custom __eq__, so equality falls back to identity
    assert d1 != d2
    # It should not be equal to a string or other sentinel
    assert d1 != "<Default>"
    assert d1 != object()


def test_default_invalid_initialization():
    """Default cannot be instantiated with arguments; should raise TypeError."""
    with pytest.raises(TypeError):
        Default(1)

import pytest
from sanic.helpers import Default


def test_default_repr_and_str():
    """Default should return the same string for repr and str."""
    d = Default()
    assert repr(d) == "<Default>"
    assert str(d) == "<Default>"
    # repr and str should be identical
    assert repr(d) == str(d)


def test_default_identity_and_equality():
    """Each Default instance is unique; identity comparison works as expected."""
    d1 = Default()
    d2 = Default()
    # Different instances are not equal by identity
    assert d1 is not d2
    # Equality falls back to identity since __eq__ is not overridden
    assert (d1 == d2) is False
    # A Default instance is equal to itself
    assert d1 == d1


def test_default_constructor_arguments():
    """Default constructor should not accept any positional or keyword arguments."""
    with pytest.raises(TypeError):
        Default(1)
    with pytest.raises(TypeError):
        Default(foo="bar")

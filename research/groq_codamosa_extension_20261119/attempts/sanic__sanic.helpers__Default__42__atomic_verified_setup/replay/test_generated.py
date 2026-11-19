import pytest
from sanic.helpers import Default


def test_default_repr_and_str():
    """`repr` and `str` should return the same sentinel representation."""
    d = Default()
    assert repr(d) == "<Default>"
    assert str(d) == "<Default>"


def test_default_identity_and_equality():
    """Each `Default` instance is unique and not equal to other objects."""
    d1 = Default()
    d2 = Default()
    # Identity: two separate instances
    assert d1 is not d2
    # Equality: default has no custom __eq__, so identity is used
    assert d1 != d2
    # Not equal to None or a generic object()
    assert d1 != None
    assert d1 != object()


def test_default_as_sentinel_in_function(tmp_path):
    """`Default` can be used as a sentinel value in function arguments."""
    sentinel = Default()

    def func(arg=sentinel):
        if arg is sentinel:
            return "sentinel"
        return arg

    # When no argument is passed, sentinel is used
    assert func() == "sentinel"
    # When a value is passed, that value is returned
    assert func(42) == 42
    # Passing None explicitly should return None, not sentinel
    assert func(None) is None

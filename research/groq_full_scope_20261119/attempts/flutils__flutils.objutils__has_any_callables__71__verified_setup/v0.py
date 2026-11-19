import pytest
from flutils.objutils import has_any_callables


def test_has_any_callables_normal():
    """When the object has at least one callable attribute among the given names,
    the function returns True."""
    # A dict has the callable method 'get'
    assert has_any_callables(dict(), "get", "keys", "nonexistent") is True
    # A list has the callable method 'append'
    assert has_any_callables([], "append", "pop") is True
    # A custom object with a callable attribute
    class C:
        def foo(self):  # callable
            pass
    assert has_any_callables(C(), "foo", "bar") is True


def test_has_any_callables_boundary():
    """When none of the specified attributes exist or are callable,
    the function returns False."""
    # A dict has no attribute 'nonexistent'
    assert has_any_callables(dict(), "nonexistent") is False
    # An object with a non-callable attribute
    class D:
        bar = 42  # not callable
    assert has_any_callables(D(), "bar") is False
    # Empty attribute list should also return False
    assert has_any_callables(dict(), *[]) is False


def test_has_any_callables_error():
    """Passing a non-string attribute name should raise a TypeError."""
    with pytest.raises(TypeError):
        has_any_callables(dict(), 123)  # non-string attribute name

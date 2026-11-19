import pytest
from flutils.objutils import has_callables


def test_has_callables_with_builtin_dict():
    """
    Normal case: a built‑in dict has all the requested attributes and they are callable.
    """
    assert has_callables(dict(), "get", "keys", "items", "values") is True


def test_has_callables_missing_attribute():
    """
    Boundary case: when one of the requested attributes is missing, the function returns False.
    """
    class Dummy:
        def foo(self):  # only one callable attribute
            pass

    # 'bar' does not exist on Dummy
    assert has_callables(Dummy(), "foo", "bar") is False


def test_has_callables_non_callable_attribute():
    """
    Error case: when an existing attribute is not callable, the function returns False.
    """
    class Dummy:
        foo = 42  # non‑callable attribute

    assert has_callables(Dummy(), "foo") is False

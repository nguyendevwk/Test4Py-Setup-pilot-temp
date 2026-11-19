import pytest
from flutils.objutils import has_callables


def test_has_callables_with_builtin_dict():
    """
    Normal case: a built‑in dict has all the requested attributes and they are callable.
    """
    assert has_callables(dict(), "get", "keys", "items", "values") is True


def test_has_callables_with_no_attributes():
    """
    Boundary case: passing no attribute names should return True because there is nothing to check.
    """
    assert has_callables(object(), *()) is True


def test_has_callables_with_missing_or_non_callable_attribute():
    """
    Error case: if an attribute is missing or not callable, the function should return False.
    """
    class Dummy:
        existing = 42  # not callable

    # Missing attribute
    assert has_callables(Dummy(), "missing") is False

    # Existing but not callable
    assert has_callables(Dummy(), "existing") is False

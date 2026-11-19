import pytest
from flutils.objutils import has_callables


def test_has_callables_true_for_builtin_methods():
    """
    Verify that has_callables returns True when all requested attributes exist
    and are callable on a built‑in type.
    """
    # dict has callable methods 'get', 'keys', 'items', 'values'
    assert has_callables(dict(), "get", "keys", "items", "values") is True
    # list has callable methods 'append', 'pop', 'clear'
    assert has_callables(list(), "append", "pop", "clear") is True
    # empty attrs should return True (no attributes to check)
    assert has_callables(object(), "") is True


def test_has_callables_false_when_attribute_missing():
    """
    Verify that has_callables returns False when any requested attribute
    does not exist on the object.
    """
    # 'nonexistent' is not an attribute of dict
    assert has_callables(dict(), "get", "nonexistent") is False
    # 'append' is not an attribute of int
    assert has_callables(42, "append") is False


def test_has_callables_false_when_attribute_not_callable():
    """
    Verify that has_callables returns False when an existing attribute
    is not callable.
    """
    class Dummy:
        x = 10  # non‑callable attribute

    dummy = Dummy()
    # 'x' exists but is not callable
    assert has_callables(dummy, "x") is False
    # mix of callable and non‑callable attributes
    assert has_callables(dummy, "x", "append") is False

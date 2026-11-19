import pytest
from flutils.objutils import has_callables

def test_has_callables_true_for_builtin_dict():
    # A dict has the attributes 'get', 'keys', 'items', 'values' and they are callable
    assert has_callables(dict(), "get", "keys", "items", "values") is True

def test_has_callables_false_when_attribute_not_callable():
    # Create a simple class with a non-callable attribute
    class Dummy:
        def method(self): pass
        value = 42  # not callable

    # 'value' is present but not callable, so the function should return False
    assert has_callables(Dummy(), "method", "value") is False

def test_has_callables_false_when_attribute_missing():
    # Using a list, which does not have the attribute 'append' as a method (it does, but test missing)
    class NoAppend:
        pass

    # 'missing' attribute does not exist, so the function should return False
    assert has_callables(NoAppend(), "missing") is False

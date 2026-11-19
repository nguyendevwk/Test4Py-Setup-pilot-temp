import pytest
from flutils.objutils import has_callables

def test_has_callables_all_present_and_callable():
    # A dict has all the listed methods and they are callable
    assert has_callables(dict(), "get", "keys", "items", "values") is True

def test_has_callables_missing_attribute_returns_false():
    # A list does not have the 'get' attribute, so the result should be False
    assert has_callables(list(), "append", "get") is False

def test_has_callables_non_callable_attribute_returns_false():
    # Create a simple class with a non-callable attribute
    class Dummy:
        def __init__(self):
            self.value = 42  # non-callable attribute

    dummy = Dummy()
    # 'value' exists but is not callable, so the function should return False
    assert has_callables(dummy, "value") is False

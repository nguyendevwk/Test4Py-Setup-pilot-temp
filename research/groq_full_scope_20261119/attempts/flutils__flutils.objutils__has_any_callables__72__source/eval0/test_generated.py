import pytest
from flutils.objutils import has_any_callables

def test_has_any_callables_true_for_callable_attribute():
    # A dict has a callable attribute 'get'
    assert has_any_callables(dict(), 'get', 'nonexistent') is True

def test_has_any_callables_false_when_no_callable_attributes():
    # A dict has no callable attributes among the given names
    assert has_any_callables(dict(), 'foo', 'bar') is False

def test_has_any_callables_false_when_attribute_exists_but_not_callable():
    class Dummy:
        foo = 42  # not callable

    dummy = Dummy()
    assert has_any_callables(dummy, 'foo', 'bar') is False

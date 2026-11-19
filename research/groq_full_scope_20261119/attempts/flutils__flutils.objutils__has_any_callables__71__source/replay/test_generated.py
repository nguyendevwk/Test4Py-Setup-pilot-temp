import pytest
from flutils.objutils import has_any_callables


def test_has_any_callables_true_for_builtin_methods():
    # A dict has several callable attributes; at least one should be found.
    assert has_any_callables(dict(), "get", "keys", "items", "values", "foo") is True


def test_has_any_callables_false_when_no_attrs_present():
    # An empty list has no attributes named 'foo' or 'bar'.
    assert has_any_callables([], "foo", "bar") is False


def test_has_any_callables_false_when_attrs_not_callable():
    class Dummy:
        foo = 42          # not callable
        bar = "string"    # not callable

    dummy = Dummy()
    # Even though attributes exist, they are not callable, so result should be False.
    assert has_any_callables(dummy, "foo", "bar") is False

import pytest
from flutils.objutils import has_any_attrs

class Dummy:
    def __init__(self):
        self.existing = 42
    def method(self):
        pass

def test_has_any_attrs_with_builtin_and_custom():
    # Built-in dict has 'keys' and 'items', custom Dummy has 'existing' and 'method'
    assert has_any_attrs({}, 'keys', 'nonexistent') is True
    assert has_any_attrs(Dummy(), 'nonexistent', 'existing') is True
    assert has_any_attrs(Dummy(), 'method', 'nonexistent') is True

def test_has_any_attrs_no_match_returns_false():
    # No attribute matches any of the provided names
    assert has_any_attrs([], 'foo', 'bar') is False
    assert has_any_attrs(123, 'bit_length', 'nonexistent') is False

def test_has_any_attrs_empty_attrs_returns_false():
    # When no attribute names are supplied, the function should return False
    assert has_any_attrs(object(), ()) is False
    assert has_any_attrs(object(),) is False

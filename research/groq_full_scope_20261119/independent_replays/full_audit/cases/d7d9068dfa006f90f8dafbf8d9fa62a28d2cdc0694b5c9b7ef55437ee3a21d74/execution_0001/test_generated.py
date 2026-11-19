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

def test_has_any_attrs_no_match_and_empty_attrs():
    # No attribute matches
    assert has_any_attrs([], 'nonexistent', 'another') is False
    # Empty attrs list should return False
    assert has_any_attrs((),) is False

def test_has_any_attrs_error_on_invalid_obj():
    # Passing an integer and a string attribute should raise no error but return False
    assert has_any_attrs(123, 'nonexistent') is False
    # Passing a None object should also return False
    assert has_any_attrs(None, 'nonexistent') is False

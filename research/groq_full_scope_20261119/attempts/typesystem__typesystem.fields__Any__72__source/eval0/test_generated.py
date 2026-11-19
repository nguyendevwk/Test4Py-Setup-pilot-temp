import pytest
from typesystem.fields import Any

def test_any_returns_same_value():
    """Any.validate should return the exact value passed in."""
    field = Any()
    value = {"key": "value"}
    result = field.validate(value)
    assert result is value  # identity check
    assert result == {"key": "value"}

def test_any_accepts_none_and_empty_string():
    """Any.validate should accept None and empty string without error."""
    field = Any()
    assert field.validate(None) is None
    assert field.validate("") == ""

def test_any_accepts_complex_objects():
    """Any.validate should accept complex objects like lists and custom classes."""
    field = Any()
    class Dummy:
        def __init__(self, x):
            self.x = x
    dummy = Dummy(42)
    assert field.validate(dummy) is dummy
    assert field.validate([1, 2, 3]) == [1, 2, 3]

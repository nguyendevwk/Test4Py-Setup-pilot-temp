import pytest
from typesystem.fields import Any

def test_any_returns_same_value():
    """Any.validate should return the exact same object passed in."""
    field = Any()
    obj = {"key": "value"}
    result = field.validate(obj)
    assert result is obj  # identity check
    assert result == {"key": "value"}  # value equality

def test_any_accepts_none_and_other_types():
    """Any.validate should accept None, integers, strings, lists, etc."""
    field = Any()
    for value in [None, 42, "hello", [1, 2, 3], (4, 5), set([6, 7])]:
        assert field.validate(value) == value

def test_any_does_not_raise_on_invalid_input():
    """Any.validate should never raise ValidationError regardless of input."""
    field = Any()
    # Using a custom object that might normally fail validation in other fields
    class Weird:
        def __repr__(self):
            return "WeirdObject"
    weird = Weird()
    try:
        result = field.validate(weird)
    except Exception as exc:
        pytest.fail(f"Any.validate raised an exception: {exc}")
    else:
        assert result is weird

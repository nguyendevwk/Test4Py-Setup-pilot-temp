import pytest
from typesystem.fields import Any

def test_any_returns_same_value():
    """Any.validate should return the exact value passed in."""
    field = Any()
    sample = {"key": [1, 2, 3], "nested": {"a": 1}}
    result = field.validate(sample)
    assert result is sample  # identity, not just equality

def test_any_accepts_none_and_empty_string():
    """Any.validate should accept None and empty string without error."""
    field = Any()
    assert field.validate(None) is None
    assert field.validate("") == ""

def test_any_accepts_complex_objects_and_functions():
    """Any.validate should work with arbitrary callables and objects."""
    field = Any()
    def dummy_func(x): return x * 2
    class Dummy:
        def __repr__(self): return "<Dummy>"
    dummy_obj = Dummy()
    assert field.validate(dummy_func) is dummy_func
    assert field.validate(dummy_obj) is dummy_obj

import pytest
from typesystem.composites import OneOf
from typesystem.fields import Int, String, Field

# Helper field that validates against a specific type
class TypeField(Field):
    def __init__(self, typ, **kwargs):
        super().__init__(**kwargs)
        self.typ = typ

    def validate(self, value):
        if isinstance(value, self.typ):
            return value
        raise ValueError(f"Expected {self.typ.__name__}")

    def validate_or_error(self, value):
        try:
            return self.validate(value), None
        except Exception as e:
            return None, e

def test_oneof_exact_match():
    """Value matches exactly one of the child fields."""
    one_of = OneOf([TypeField(int), TypeField(str)])
    result = one_of.validate(42)
    assert result == 42

def test_oneof_multiple_matches():
    """Value matches more than one child field, should raise validation error."""
    one_of = OneOf([TypeField(int), TypeField(int)])
    with pytest.raises(Exception) as exc:
        one_of.validate(10)
    assert "multiple_matches" in str(exc.value)

def test_oneof_no_match():
    """Value matches none of the child fields, should raise validation error."""
    one_of = OneOf([TypeField(int), TypeField(str)])
    with pytest.raises(Exception) as exc:
        one_of.validate(3.14)
    assert "no_match" in str(exc.value)

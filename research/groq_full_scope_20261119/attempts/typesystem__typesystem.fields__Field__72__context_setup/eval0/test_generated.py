import pytest
from typesystem.fields import Union, Field, ValidationError, ValidationResult

# Simple concrete Field for testing purposes
class DummyField(Field):
    errors = {"type": "Expected int, got {value}."}

    def validate(self, value):
        if not isinstance(value, int):
            raise self.validation_error("type")
        return value

def test_union_accepts_valid_int():
    """Union should accept a value that matches one of its child fields."""
    int_field = DummyField()
    union = Union(any_of=[int_field])
    result = union.validate_or_error(42)
    assert isinstance(result, ValidationResult)
    assert result.error is None
    assert result.value == 42

def test_union_null_handling():
    """Union should allow None when any child allows null."""
    int_field = DummyField()
    null_field = DummyField(allow_null=True)
    union = Union(any_of=[int_field, null_field])
    # None should be accepted because one child allows null
    result = union.validate_or_error(None)
    assert isinstance(result, ValidationResult)
    assert result.error is None
    assert result.value is None

def test_union_error_when_no_match():
    """Union should raise a union error when no child validates the value."""
    int_field = DummyField()
    union = Union(any_of=[int_field])
    with pytest.raises(ValidationError) as excinfo:
        union.validate_or_error("not an int")
    # The error should be the union error, not the child type error
    assert excinfo.value.code == "union"
    assert "Did not match any valid type." in str(excinfo.value)

import pytest
from typesystem.fields import Union, Field
from typesystem.base import ValidationError, ValidationResult

# Simple concrete Field implementation for testing
class IntField(Field):
    errors = {"type": "Expected an integer."}

    def validate(self, value):
        if isinstance(value, int):
            return value
        raise self.validation_error("type")

class StrField(Field):
    errors = {"type": "Expected a string."}

    def validate(self, value):
        if isinstance(value, str):
            return value
        raise self.validation_error("type")

def test_union_accepts_valid_child():
    """Union should validate when one child matches."""
    union = Union(any_of=[IntField(), StrField()])
    result = union.validate_or_error(42)
    assert isinstance(result, ValidationResult)
    assert result.error is None
    assert result.value == 42

def test_union_null_handling_and_error_message():
    """Union should allow null if any child allows it, otherwise raise error."""
    int_field = IntField(allow_null=True)
    str_field = StrField()
    union = Union(any_of=[int_field, str_field])
    # Null is allowed because int_field allows null
    assert union.validate_or_error(None).value is None

    # Create a union without any allow_null child
    union_no_null = Union(any_of=[IntField(), StrField()])
    with pytest.raises(ValidationError) as excinfo:
        union_no_null.validate_or_error(None)
    assert "May not be null." in str(excinfo.value)

def test_union_fallback_to_union_error():
    """When no child validates, Union should raise its own error."""
    union = Union(any_of=[IntField(), StrField()])
    with pytest.raises(ValidationError) as excinfo:
        union.validate_or_error(3.14)  # float is invalid for both
    # The error should come from the Union itself, not from a child
    assert "Did not match any valid type." in str(excinfo.value)

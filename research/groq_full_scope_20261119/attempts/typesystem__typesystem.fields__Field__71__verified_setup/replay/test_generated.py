import pytest
from typesystem.fields import Field
from typesystem.base import ValidationError, ValidationResult

# A minimal concrete Field implementation for testing purposes
class IntField(Field):
    errors = {"invalid": "Value must be an integer"}

    def validate(self, value):
        if value is None and self.allow_null:
            return None
        if isinstance(value, int):
            return value
        raise self.validation_error("invalid")

def test_int_field_validates_integer():
    f = IntField()
    result = f.validate_or_error(42)
    assert isinstance(result, ValidationResult)
    assert result.error is None
    assert result.value == 42

def test_int_field_allows_null_when_allowed():
    f = IntField(allow_null=True)
    result = f.validate_or_error(None)
    assert isinstance(result, ValidationResult)
    assert result.error is None
    assert result.value is None

def test_int_field_raises_validation_error_on_invalid_type():
    f = IntField()
    with pytest.raises(ValidationError) as excinfo:
        f.validate("not an int")
    assert "Value must be an integer" in str(excinfo.value)
    # Also test validate_or_error returns a ValidationResult with error
    result = f.validate_or_error("not an int")
    assert result.error is not None
    assert isinstance(result.error, ValidationError)
    assert result.value is None

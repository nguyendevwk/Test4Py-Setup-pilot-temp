import pytest
from typesystem.fields import Field
from typesystem.base import ValidationError, ValidationResult

class DummyField(Field):
    errors = {"invalid": "Invalid value: {value}"}

    def validate(self, value):
        if value is None:
            raise ValidationError(text="None not allowed", code="none")
        if not isinstance(value, int):
            raise ValidationError(text="Not an int", code="type")
        return value

def test_default_and_get_default_value():
    # default is set via keyword, callable default returns new value each call
    field = DummyField(default=lambda: 42)
    assert field.has_default() is True
    assert field.get_default_value() == 42
    # default is not callable
    field2 = DummyField(default=10)
    assert field2.get_default_value() == 10

def test_validate_or_error_success_and_failure():
    field = DummyField()
    # valid integer passes
    result = field.validate_or_error(5)
    assert isinstance(result, ValidationResult)
    assert result.error is None
    assert result.value == 5
    # invalid type triggers ValidationError
    result2 = field.validate_or_error("foo")
    assert isinstance(result2, ValidationResult)
    assert result2.error is not None
    assert isinstance(result2.error, ValidationError)
    assert result2.error.code == "type"
    assert result2.value is None

def test_validation_error_and_get_error_text():
    field = DummyField()
    # trigger a validation error manually
    error = field.validation_error("invalid")
    assert isinstance(error, ValidationError)
    assert error.code == "invalid"
    # get_error_text uses field's __dict__ for formatting
    field.title = "TestField"
    field.description = "A test"
    text = field.get_error_text("invalid")
    assert text == "Invalid value: {value}".format(**field.__dict__)

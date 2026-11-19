import pytest
from typesystem.formats import BaseFormat
from typesystem.base import ValidationError

class IntFormat(BaseFormat):
    errors = {"not_int": "Expected an int, got {value}"}

    def is_native_type(self, value):
        return isinstance(value, int)

    def validate(self, value):
        if self.is_native_type(value):
            return value
        return self.validation_error("not_int")

    def serialize(self, obj):
        return str(obj) if obj is not None else None

def test_validation_error_message():
    fmt = IntFormat()
    err = fmt.validation_error("not_int")
    assert isinstance(err, ValidationError)
    assert err.code == "not_int"
    assert err.text == "Expected an int, got {value}"
    # The message should include the current state of the format instance
    fmt.value = 42
    err_with_value = fmt.validation_error("not_int")
    assert err_with_value.text == "Expected an int, got 42"

def test_validate_success():
    fmt = IntFormat()
    result = fmt.validate(10)
    assert result == 10
    assert fmt.is_native_type(result) is True
    serialized = fmt.serialize(result)
    assert serialized == "10"

def test_validate_error():
    fmt = IntFormat()
    result = fmt.validate("not an int")
    assert isinstance(result, ValidationError)
    assert result.code == "not_int"
    assert result.text == "Expected an int, got {value}"

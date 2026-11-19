import pytest
from typesystem.formats import BaseFormat
from typesystem.base import ValidationError


class DummyFormat(BaseFormat):
    errors = {"not_int": "Value {value} is not an integer"}

    def is_native_type(self, value):
        return isinstance(value, int)

    def validate(self, value):
        if not self.is_native_type(value):
            return self.validation_error("not_int")
        return value

    def serialize(self, obj):
        if not self.is_native_type(obj):
            return None
        return str(obj)


def test_validation_error_message_and_code():
    fmt = DummyFormat()
    fmt.value = 3.14  # set attribute used in error formatting
    error = fmt.validation_error("not_int")
    assert isinstance(error, ValidationError)
    assert error.code == "not_int"
    assert error.text == "Value 3.14 is not an integer"


def test_validate_returns_value_or_error():
    fmt = DummyFormat()
    # Valid integer
    result = fmt.validate(42)
    assert result == 42
    # Invalid type triggers ValidationError
    result = fmt.validate("not an int")
    assert isinstance(result, ValidationError)
    assert result.code == "not_int"
    assert result.text == "Value not an int is not an integer"


def test_serialize_returns_string_or_none():
    fmt = DummyFormat()
    # Serialize valid integer
    assert fmt.serialize(7) == "7"
    # Serialize invalid type returns None
    assert fmt.serialize(3.14) is None

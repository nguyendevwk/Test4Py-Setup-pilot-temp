import pytest
from typesystem.formats import BaseFormat
from typesystem.base import ValidationError

# A minimal concrete subclass for testing purposes
class DummyFormat(BaseFormat):
    errors = {"type_error": "Expected {expected_type}, got {actual_type}"}

    def is_native_type(self, value):
        return isinstance(value, int)

    def validate(self, value):
        if self.is_native_type(value):
            return value
        return self.validation_error("type_error")

    def serialize(self, obj):
        return str(obj) if obj is not None else None


def test_validation_error_message_and_code():
    fmt = DummyFormat()
    fmt.expected_type = "int"
    fmt.actual_type = "str"
    err = fmt.validation_error("type_error")
    assert isinstance(err, ValidationError)
    assert err.code == "type_error"
    assert err.text == "Expected int, got str"


def test_is_native_type_and_validate_success_and_failure(tmp_path):
    fmt = DummyFormat()
    # Successful validation
    assert fmt.is_native_type(42) is True
    assert fmt.validate(42) == 42
    # Failure validation
    assert fmt.is_native_type("not an int") is False
    err = fmt.validate("not an int")
    assert isinstance(err, ValidationError)
    assert err.code == "type_error"
    assert err.text == "Expected int, got str"


def test_serialize_returns_string_or_none():
    fmt = DummyFormat()
    # Serialize a normal value
    assert fmt.serialize(123) == "123"
    # Serialize None
    assert fmt.serialize(None) is None

import pytest
from typesystem.formats import BaseFormat
from typesystem.base import ValidationError


class DummyFormat(BaseFormat):
    errors = {"not_int": "Expected an integer, got {value}"}

    def is_native_type(self, value):
        return isinstance(value, int)

    def validate(self, value):
        if not self.is_native_type(value):
            return self.validation_error("not_int")
        return value

    def serialize(self, obj):
        return str(obj)


def test_validation_error_message():
    fmt = DummyFormat()
    fmt.value = "abc"
    err = fmt.validation_error("not_int")
    assert isinstance(err, ValidationError)
    assert err.code == "not_int"
    assert err.text == "Expected an integer, got abc"


def test_abstract_methods_raise():
    base = BaseFormat()
    with pytest.raises(NotImplementedError):
        base.is_native_type(1)
    with pytest.raises(NotImplementedError):
        base.validate(1)
    with pytest.raises(NotImplementedError):
        base.serialize(1)


def test_subclass_validate_and_serialize():
    fmt = DummyFormat()
    # Valid integer
    assert fmt.validate(42) == 42
    # Invalid type triggers ValidationError
    result = fmt.validate("not an int")
    assert isinstance(result, ValidationError)
    assert result.code == "not_int"
    # Serialization
    assert fmt.serialize(123) == "123"

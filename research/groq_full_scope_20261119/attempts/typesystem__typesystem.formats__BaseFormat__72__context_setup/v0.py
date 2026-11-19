import pytest
from typesystem.formats import BaseFormat
from typesystem.base import ValidationError


class DummyFormat(BaseFormat):
    errors = {"not_native": "Value {value} is not a native type"}

    def is_native_type(self, value):
        return isinstance(value, int)

    def validate(self, value):
        if not self.is_native_type(value):
            return self.validation_error("not_native")
        return value

    def serialize(self, obj):
        if not self.is_native_type(obj):
            raise ValidationError("Cannot serialize non-native type")
        return str(obj)


def test_validation_error_message_and_code():
    fmt = DummyFormat()
    fmt.value = 3.14  # set attribute used in error formatting
    error = fmt.validation_error("not_native")
    assert isinstance(error, ValidationError)
    assert error.code == "not_native"
    assert error.text == "Value 3.14 is not a native type"


def test_is_native_type_and_validate_behavior():
    fmt = DummyFormat()
    # native type
    assert fmt.is_native_type(42) is True
    assert fmt.validate(42) == 42
    # non-native type triggers ValidationError
    result = fmt.validate("hello")
    assert isinstance(result, ValidationError)
    assert result.code == "not_native"
    assert result.text == "Value hello is not a native type"


def test_abstract_methods_raise_not_implemented():
    class IncompleteFormat(BaseFormat):
        pass

    inc = IncompleteFormat()
    with pytest.raises(NotImplementedError):
        inc.is_native_type(1)
    with pytest.raises(NotImplementedError):
        inc.validate(1)
    with pytest.raises(NotImplementedError):
        inc.serialize(1)

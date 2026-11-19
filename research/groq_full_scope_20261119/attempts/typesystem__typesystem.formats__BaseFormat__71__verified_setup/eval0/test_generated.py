import pytest
from typesystem.formats import BaseFormat
from typesystem.base import ValidationError


class DummyFormat(BaseFormat):
    errors = {"missing": "Field {field} is required."}

    def __init__(self, field: str):
        self.field = field

    def is_native_type(self, value):
        return isinstance(value, str)

    def validate(self, value):
        if value is None:
            return self.validation_error("missing")
        return value

    def serialize(self, obj):
        return str(obj)


def test_validation_error_formatting():
    fmt = DummyFormat(field="username")
    err = fmt.validation_error("missing")
    assert isinstance(err, ValidationError)
    assert err.code == "missing"
    assert err.text == "Field username is required."


def test_abstract_methods_raise():
    base = BaseFormat()
    with pytest.raises(NotImplementedError):
        base.is_native_type(123)
    with pytest.raises(NotImplementedError):
        base.validate(123)
    with pytest.raises(NotImplementedError):
        base.serialize(123)


def test_dummy_format_behavior(tmp_path):
    fmt = DummyFormat(field="email")
    # validate returns value when present
    assert fmt.validate("test@example.com") == "test@example.com"
    # validate returns ValidationError when None
    err = fmt.validate(None)
    assert isinstance(err, ValidationError)
    assert err.code == "missing"
    # serialize converts to string
    assert fmt.serialize(42) == "42"

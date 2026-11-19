import pytest
from typesystem.fields import Field
from typesystem.base import ValidationError, ValidationResult

# Create a minimal concrete Field subclass for testing
class DummyField(Field):
    errors = {"invalid": "Invalid value: {value}"}

    def validate(self, value):
        if value != "ok":
            raise self.validation_error("invalid")
        return value

def test_default_handling_and_get_default_value(tmp_path):
    # Field with a callable default
    def default_factory():
        return "default_value"

    f = DummyField(default=default_factory)
    assert f.has_default() is True
    assert f.get_default_value() == "default_value"

    # Field with a static default
    f2 = DummyField(default="static")
    assert f2.has_default() is True
    assert f2.get_default_value() == "static"

    # Field without default
    f3 = DummyField()
    assert f3.has_default() is False
    assert f3.get_default_value() is None

def test_validation_error_and_get_error_text():
    f = DummyField()
    # validate_or_error should return a ValidationResult with error
    result = f.validate_or_error("bad")
    assert isinstance(result.error, ValidationError)
    assert result.error.code == "invalid"
    # get_error_text should format the message correctly
    assert f.get_error_text("invalid") == "Invalid value: bad"

    # validate_or_error should succeed for valid input
    result_ok = f.validate_or_error("ok")
    assert result_ok.error is None
    assert result_ok.value == "ok"

def test_union_operator_and_any_of():
    f1 = DummyField()
    f2 = DummyField()
    # Union of two fields
    union = f1 | f2
    assert hasattr(union, "any_of")
    assert union.any_of == [f1, f2]

    # Union with an existing Union
    union2 = union | f1
    assert union2.any_of == [f1, f2, f1]

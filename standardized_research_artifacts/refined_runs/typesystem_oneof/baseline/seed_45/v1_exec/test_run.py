import pytest
from typesystem.composites import OneOf, Field


class IntField(Field):
    def validate_or_error(self, value):
        if isinstance(value, int):
            return value, None
        return None, "not int"


class StrField(Field):
    def validate_or_error(self, value):
        if isinstance(value, str):
            return value, None
        return None, "not str"


class AnyField(Field):
    def validate_or_error(self, value):
        return value, None


def test_oneof_validate_behavior():
    oneof_int_str = OneOf([IntField(), StrField()])
    assert oneof_int_str.validate(5) == 5
    assert oneof_int_str.validate("hello") == "hello"
    with pytest.raises(Exception) as excinfo:
        oneof_int_str.validate(5.0)
    assert "no_match" in str(excinfo.value)

    oneof_int_any = OneOf([IntField(), AnyField()])
    with pytest.raises(Exception) as excinfo:
        oneof_int_any.validate(5)
    assert "multiple_matches" in str(excinfo.value)

import pytest
from typesystem.composites import OneOf
from typesystem.fields import Field


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


def test_one_of_validate_behavior():
    one_of = OneOf([IntField(), StrField()])
    assert one_of.validate(5) == 5
    assert one_of.validate("hello") == "hello"
    with pytest.raises(Exception) as excinfo:
        one_of.validate(5.0)
    assert "no_match" in str(excinfo.value)

    one_of_multi = OneOf([IntField(), AnyField()])
    with pytest.raises(Exception) as excinfo:
        one_of_multi.validate(5)
    assert "multiple_matches" in str(excinfo.value)

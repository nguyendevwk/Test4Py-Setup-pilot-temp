import pytest
from typesystem.composites import OneOf
from typesystem.fields import Field


class DummyIntField(Field):
    def validate_or_error(self, value):
        if isinstance(value, int):
            return value, None
        return None, "not int"


def test_oneof_multiple_matches_raises_error():
    int_field1 = DummyIntField()
    int_field2 = DummyIntField()
    one_of = OneOf([int_field1, int_field2])
    with pytest.raises(Exception) as excinfo:
        one_of.validate(5)
    assert "Matched more than one type." in str(excinfo.value)

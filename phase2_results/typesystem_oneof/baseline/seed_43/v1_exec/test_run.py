import pytest
from typesystem.composites import OneOf

class DummyField:
    def __init__(self, match_func):
        self.match_func = match_func

    def validate_or_error(self, value):
        if self.match_func(value):
            return value, None
        return None, "error"

def test_oneof_validate_behavior():
    int_field = DummyField(lambda v: isinstance(v, int))
    str_field = DummyField(lambda v: isinstance(v, str))
    any_field = DummyField(lambda v: True)

    # Exactly one match
    oneof_int = OneOf([int_field, str_field])
    assert oneof_int.validate(42) == 42
    assert oneof_int.validate("hi") == "hi"

    # No match
    with pytest.raises(Exception) as excinfo:
        oneof_int.validate(3.14)
    assert "no_match" in str(excinfo.value)

    # Multiple matches
    oneof_multi = OneOf([int_field, any_field])
    with pytest.raises(Exception) as excinfo:
        oneof_multi.validate(10)
    assert "multiple_matches" in str(excinfo.value)

    # allow_null not allowed
    with pytest.raises(AssertionError):
        OneOf([int_field], allow_null=True)

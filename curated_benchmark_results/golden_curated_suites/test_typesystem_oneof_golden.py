import pytest
from typesystem.composites import OneOf
from typesystem.fields import String, Integer, Field


class AlwaysPass(Field):
    """A field that accepts any value without error."""
    def validate(self, value):
        return value


def test_oneof_validate_behavior():
    # OneOf with String and Integer
    schema = OneOf([String(), Integer()])

    # Valid string: matches exactly one type
    val, err = schema.validate_or_error("hello")
    assert err is None
    assert val == "hello"

    # Valid integer: matches exactly one type
    val, err = schema.validate_or_error(42)
    assert err is None
    assert val == 42

    # Multiple matches: String and AlwaysPass both accept the string
    multi_schema = OneOf([String(), AlwaysPass()])
    val, err = multi_schema.validate_or_error("duplicate")
    assert val is None
    assert err is not None
    # The error should contain the "multiple_matches" code
    codes = [m.code for m in err.messages()]
    assert "multiple_matches" in codes

    # No match: Float does not match String or Integer
    val, err = schema.validate_or_error(3.14)
    assert val is None
    assert err is not None
    # The error should contain the "no_match" code
    codes = [m.code for m in err.messages()]
    assert "no_match" in codes

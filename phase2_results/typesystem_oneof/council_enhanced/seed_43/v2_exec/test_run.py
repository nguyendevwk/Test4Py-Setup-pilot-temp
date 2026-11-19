import pytest
from typesystem.composites import OneOf
from typesystem.fields import String, Integer
from typesystem.base import ValidationError


def test_oneof_validate_behavior():
    schema = OneOf([String(), Integer()])

    # Single match: string
    val, err = schema.validate_or_error("abc")
    assert err is None
    assert val == "abc"

    # Single match: integer
    val, err = schema.validate_or_error(123)
    assert err is None
    assert val == 123

    # Value that matches the first field (String) should be accepted
    val, err = schema.validate_or_error("123")
    assert err is None
    assert val == "123"

    # Multiple matches: two identical fields both accept the same value
    schema_multi = OneOf([String(), String()])
    with pytest.raises(ValidationError) as excinfo:
        schema_multi.validate_or_error("abc")
    assert excinfo.value.code == "multiple_matches"

    # Passing disallowed keyword argument raises AssertionError
    with pytest.raises(AssertionError):
        OneOf([String()], allow_null=True)

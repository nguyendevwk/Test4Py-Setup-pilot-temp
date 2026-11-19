import pytest
from typesystem.composites import OneOf
from typesystem.fields import String, Integer
from typesystem.base import ValidationError


def test_oneof_exact_match_and_error_conditions():
    schema = OneOf([String(), Integer()])

    # Exact match: string input
    val, err = schema.validate_or_error("hello")
    assert err is None
    assert isinstance(val, str)
    assert val == "hello"

    # Exact match: integer input
    val, err = schema.validate_or_error(42)
    assert err is None
    assert isinstance(val, int)
    assert val == 42

    # Multiple matches: same type twice
    multi_schema = OneOf([String(), String()])
    with pytest.raises(ValidationError) as excinfo:
        multi_schema.validate("dup")
    assert "multiple_matches" in str(excinfo.value)

    # No match: value that matches none
    with pytest.raises(ValidationError) as excinfo:
        schema.validate(None)
    assert "no_match" in str(excinfo.value)

    # validate_or_error returns a tuple (value, error) for invalid input
    val, err = schema.validate_or_error(None)
    assert isinstance(err, ValidationError)
    assert val is None

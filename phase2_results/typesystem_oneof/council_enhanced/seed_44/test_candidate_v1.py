import pytest
from typesystem.composites import OneOf
from typesystem.fields import String, Integer
from typesystem.base import ValidationError, ValidationResult


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
    assert excinfo.value.code == "multiple_matches"

    # No match: value that matches none
    with pytest.raises(ValidationError) as excinfo:
        schema.validate(None)
    assert excinfo.value.code == "no_match"

    # validate_or_error returns ValidationResult with error for invalid input
    result = schema.validate_or_error(None)
    assert isinstance(result, ValidationResult)
    assert result.error is not None
    assert result.value is None

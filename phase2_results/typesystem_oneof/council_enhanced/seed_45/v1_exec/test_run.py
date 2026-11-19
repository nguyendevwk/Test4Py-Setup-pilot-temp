import pytest
from typesystem.composites import OneOf
from typesystem.fields import String, Integer
from typesystem.base import ValidationError

def test_oneof_validation_logic():
    # Exactly one match: string
    schema = OneOf([String(), Integer()])
    val, err = schema.validate_or_error("hello")
    assert err is None
    assert val == "hello"

    # Exactly one match: integer
    val, err = schema.validate_or_error(42)
    assert err is None
    assert val == 42

    # Multiple matches: two identical String fields
    multi_schema = OneOf([String(), String()])
    with pytest.raises(ValidationError) as excinfo:
        multi_schema.validate_or_error("dup")
    assert excinfo.value.code == "multiple_matches"

    # No match: value that matches neither String nor Integer
    with pytest.raises(ValidationError) as excinfo:
        schema.validate_or_error(None)
    assert excinfo.value.code == "no_match"

    # allow_null keyword not permitted
    with pytest.raises(AssertionError):
        OneOf([String()], allow_null=True)

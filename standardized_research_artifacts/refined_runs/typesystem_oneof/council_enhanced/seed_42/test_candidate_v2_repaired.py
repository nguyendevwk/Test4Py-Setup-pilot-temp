import pytest
from typesystem.composites import OneOf
from typesystem.fields import String, Integer
from typesystem.base import ValidationError

def test_oneof_behavior():
    # Exactly one match: string
    schema = OneOf([String(), Integer()])
    val, err = schema.validate_or_error("sample_text")
    assert err is None
    assert val == "sample_text"

    # Exactly one match: integer
    val, err = schema.validate_or_error(42)
    assert err is None
    assert val == 42

    # Multiple matches: two identical String fields
    multi_schema = OneOf([String(), String()])
    with pytest.raises(ValidationError) as excinfo:
        multi_schema.validate("dup")
    assert "multiple matches" in str(excinfo.value)

    # No match: value not matching any field
    single_int_schema = OneOf([Integer()])
    with pytest.raises(ValidationError) as excinfo:
        single_int_schema.validate("not_an_int")
    assert "no match" in str(excinfo.value)

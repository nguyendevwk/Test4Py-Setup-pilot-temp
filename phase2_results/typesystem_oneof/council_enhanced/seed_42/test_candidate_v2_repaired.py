import pytest
from typesystem.composites import OneOf
from typesystem.fields import String, Integer
from typesystem.base import ValidationError


def test_oneof_validate_behavior():
    # Exactly one match: String matches, Integer does not
    schema = OneOf([String(), Integer()])
    value, error = schema.validate_or_error("sample_text")
    assert error is None
    assert value == "sample_text"

    # Multiple matches: two String fields both accept the same value
    schema_multi = OneOf([String(), String()])
    with pytest.raises(ValidationError) as excinfo:
        schema_multi.validate("sample_text")
    assert "multiple matches" in excinfo.value.message

    # No match: neither Integer nor String accepts None
    schema_none = OneOf([Integer(), String()])
    with pytest.raises(ValidationError) as excinfo:
        schema_none.validate(None)
    assert "no match" in excinfo.value.message

    # allow_null is not permitted in OneOf constructor
    with pytest.raises(AssertionError):
        OneOf([String()], allow_null=True)

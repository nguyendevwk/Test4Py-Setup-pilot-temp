import pytest
from typesystem.composites import OneOf
from typesystem.fields import String, Integer, Field
from typesystem.base import ValidationError


def test_oneof_validation_paths():
    # One match: String
    schema = OneOf([String(), Integer()])
    val, err = schema.validate_or_error("sample_text")
    assert err is None
    assert val == "sample_text"

    # No match: float value
    val, err = schema.validate_or_error(3.14)
    assert err is not None
    assert isinstance(err, ValidationError)
    assert err.error_code == "no_match"

    # Multiple matches: two dummy fields that accept any value
    class DummyField(Field):
        def validate(self, value):
            return value

    dummy1, dummy2 = DummyField(), DummyField()
    schema_multi = OneOf([dummy1, dummy2])
    val, err = schema_multi.validate_or_error("anything")
    assert err is not None
    assert isinstance(err, ValidationError)
    assert err.error_code == "multiple_matches"

    # Direct validate call propagates ValidationError
    with pytest.raises(ValidationError) as excinfo:
        schema_multi.validate("anything")
    assert excinfo.value.error_code == "multiple_matches"

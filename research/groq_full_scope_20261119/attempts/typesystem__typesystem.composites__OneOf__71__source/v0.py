import pytest
from typesystem.composites import OneOf
from typesystem.fields import Integer, String, Any


def test_oneof_matches_exactly_one_type():
    """Value should be accepted when it matches exactly one of the sub-fields."""
    field = OneOf([Integer(), String()])
    # Integer matches only the Integer field
    result = field.validate(42)
    assert result == 42
    # String matches only the String field
    result = field.validate("hello")
    assert result == "hello"


def test_oneof_no_match_raises_error():
    """Value should raise a validation error when it matches none of the sub-fields."""
    field = OneOf([Integer(), String()])
    with pytest.raises(field.ValidationError) as excinfo:
        field.validate(3.14)
    assert "no_match" in str(excinfo.value)


def test_oneof_multiple_matches_raises_error():
    """Value should raise a validation error when it matches more than one sub-field."""
    # Using Integer twice will cause a value to match both sub-fields
    field = OneOf([Integer(), Integer()])
    with pytest.raises(field.ValidationError) as excinfo:
        field.validate(10)
    assert "multiple_matches" in str(excinfo.value)

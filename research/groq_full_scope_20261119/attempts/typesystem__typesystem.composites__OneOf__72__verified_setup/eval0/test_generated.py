import pytest
from typesystem.composites import OneOf
from typesystem.fields import Int, String, Any

def test_oneof_single_match():
    """Value matches exactly one child field."""
    field = OneOf([Int(), String()])
    result = field.validate(42)
    assert result == 42  # Int field returns the validated value unchanged

def test_oneof_multiple_match():
    """Value matches more than one child field, should raise multiple_matches."""
    field = OneOf([Int(), Any()])
    with pytest.raises(field.validation_error.__class__) as excinfo:
        field.validate(10)
    assert "multiple_matches" in str(excinfo.value)

def test_oneof_no_match():
    """Value matches none of the child fields, should raise no_match."""
    field = OneOf([Int(), String()])
    with pytest.raises(field.validation_error.__class__) as excinfo:
        field.validate(3.14)  # float does not match Int or String
    assert "no_match" in str(excinfo.value)

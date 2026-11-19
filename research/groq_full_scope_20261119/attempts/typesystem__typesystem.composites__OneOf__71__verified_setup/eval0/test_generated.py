import pytest
from typesystem.composites import OneOf
from typesystem.fields import Int, Str, Any


def test_oneof_single_match():
    """Value matches exactly one of the provided fields."""
    field = OneOf([Int(), Str()])
    # Int matches, Str does not
    result = field.validate(42)
    assert result == 42
    # Str matches, Int does not
    result = field.validate("hello")
    assert result == "hello"


def test_oneof_multiple_matches():
    """Value matches more than one field, should raise validation error."""
    field = OneOf([Int(), Any()])
    with pytest.raises(field.ValidationError) as excinfo:
        field.validate(10)
    assert "multiple_matches" in str(excinfo.value)


def test_oneof_no_match():
    """Value matches none of the fields, should raise validation error."""
    field = OneOf([Int(), Str()])
    with pytest.raises(field.ValidationError) as excinfo:
        field.validate(3.14)
    assert "no_match" in str(excinfo.value)

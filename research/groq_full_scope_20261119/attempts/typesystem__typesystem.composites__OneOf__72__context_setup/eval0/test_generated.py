import pytest
from typesystem.composites import OneOf
from typesystem.fields import Any, Int, String


def test_oneof_exact_match():
    """Value matches exactly one of the sub-fields."""
    field = OneOf([Int(), String()])
    # Integer matches Int only
    assert field.validate(42) == 42
    # String matches String only
    assert field.validate("hello") == "hello"


def test_oneof_multiple_matches():
    """Value matches more than one sub-field triggers multiple_matches error."""
    field = OneOf([Any(), Int()])
    with pytest.raises(Exception) as excinfo:
        field.validate(10)
    assert "multiple_matches" in str(excinfo.value)


def test_oneof_no_match():
    """Value matches none of the sub-fields triggers no_match error."""
    field = OneOf([Int(), String()])
    with pytest.raises(Exception) as excinfo:
        field.validate(3.14)
    assert "no_match" in str(excinfo.value)

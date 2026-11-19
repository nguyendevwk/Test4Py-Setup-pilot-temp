import pytest
from typesystem.fields import Any, Int, Field
from typesystem.composites import Not


def test_not_rejects_value_that_matches_negated():
    """Not should raise a validation error when the negated field accepts the value."""
    not_field = Not(Int())
    with pytest.raises(Field.ValidationError) as excinfo:
        not_field.validate(42)  # 42 is a valid int, so Not should reject it
    assert "Must not match." in str(excinfo.value)


def test_not_accepts_value_that_does_not_match_negated():
    """Not should accept values that the negated field rejects."""
    not_field = Not(Int())
    # 3.14 is not an int, so Int rejects it; Not should accept it
    result = not_field.validate(3.14)
    assert result == 3.14


def test_not_accepts_null_when_negated_rejects_null():
    """Not should accept None if the negated field rejects it."""
    not_field = Not(Int())
    # Int rejects None; Not should accept it
    result = not_field.validate(None)
    assert result is None

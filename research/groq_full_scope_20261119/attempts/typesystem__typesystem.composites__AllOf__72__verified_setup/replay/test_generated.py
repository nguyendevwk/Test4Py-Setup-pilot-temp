import pytest
from typesystem.composites import AllOf
from typesystem.fields import Any, Field


class DummyField(Field):
    """A field that rejects the value 0."""

    def validate(self, value):
        if value == 0:
            raise ValueError("Zero is not allowed")
        return value


def test_allof_valid_value_passes():
    """AllOf should accept a value that satisfies all child fields."""
    all_of_field = AllOf(all_of=[Any(), DummyField()])
    # Any accepts anything, DummyField accepts non-zero
    result = all_of_field.validate(42)
    assert result == 42  # value is returned unchanged


def test_allof_invalid_value_raises():
    """AllOf should raise if any child field raises."""
    all_of_field = AllOf(all_of=[Any(), DummyField()])
    with pytest.raises(ValueError, match="Zero is not allowed"):
        all_of_field.validate(0)


def test_allof_empty_children_no_validation():
    """AllOf with no children should perform no validation and return the value."""
    all_of_field = AllOf(all_of=[])
    # No child fields, so any value should pass
    for val in [None, 0, "test", 3.14]:
        assert all_of_field.validate(val) == val

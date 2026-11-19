import pytest
from typesystem.composites import AllOf
from typesystem.fields import Any, Field


class FailingField(Field):
    """A field that always fails validation."""
    def validate(self, value):
        raise ValueError("validation failed")


def test_allof_passes_with_any_fields():
    """AllOf should accept any value when composed of Any fields."""
    all_of = AllOf(all_of=[Any(), Any()])
    # Any field accepts any value, so validation should succeed for various types
    for val in [None, 42, "hello", [1, 2], {"a": 1}]:
        assert all_of.validate(val) is val


def test_allof_accepts_empty_list():
    """AllOf with an empty list should simply return the value unchanged."""
    all_of = AllOf(all_of=[])
    for val in [None, 0, "", [], {}]:
        assert all_of.validate(val) is val


def test_allof_propagates_child_error():
    """AllOf should raise the exception from the first failing child."""
    all_of = AllOf(all_of=[Any(), FailingField(), Any()])
    with pytest.raises(ValueError, match="validation failed"):
        all_of.validate("test")

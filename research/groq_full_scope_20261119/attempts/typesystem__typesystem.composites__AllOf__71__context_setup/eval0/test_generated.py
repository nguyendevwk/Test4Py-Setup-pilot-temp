import pytest
from typesystem.composites import AllOf
from typesystem.fields import Field, ValidationError


class DummyField(Field):
    """A simple Field that validates that the value equals a preset expected value."""

    def __init__(self, expected, **kwargs):
        super().__init__(**kwargs)
        self.expected = expected

    def validate(self, value):
        if value != self.expected:
            raise ValidationError(f"Expected {self.expected!r}, got {value!r}")
        return value


class RaisingField(Field):
    """A Field that always raises ValidationError."""

    def validate(self, value):
        raise ValidationError("always fails")


def test_allof_normal_behavior():
    """AllOf should validate when all child fields succeed."""
    field_a = DummyField(expected=42)
    field_b = DummyField(expected=42)
    all_of = AllOf(all_of=[field_a, field_b])
    result = all_of.validate(42)
    assert result == 42  # value is returned unchanged


def test_allof_empty_list_boundary():
    """AllOf with an empty list should accept any value and return it unchanged."""
    all_of = AllOf(all_of=[])
    for value in (None, 0, "test", [1, 2, 3]):
        assert all_of.validate(value) == value


def test_allof_child_validation_error():
    """AllOf should propagate ValidationError from any child field."""
    field_a = DummyField(expected=1)
    field_b = RaisingField()
    all_of = AllOf(all_of=[field_a, field_b])
    with pytest.raises(ValidationError) as excinfo:
        all_of.validate(1)
    assert "always fails" in str(excinfo.value)

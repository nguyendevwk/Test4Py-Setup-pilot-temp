import pytest
from typesystem.fields import Array, Field
from typesystem.base import ValidationError


class IntField(Field):
    """Simple field that validates integers."""

    def validate(self, value):
        if not isinstance(value, int):
            raise ValidationError(text="Must be an integer.", code="type")
        return value


def test_array_normal_validation_and_serialization():
    """Array with a single item type and min_items constraint."""
    arr_field = Array(items=IntField(), min_items=2)
    # Valid input: list of two integers
    result = arr_field.validate([1, 2])
    assert result == [1, 2]
    # Serialization should preserve the values
    serialized = arr_field.serialize(result)
    assert serialized == [1, 2]
    # Invalid input: too few items
    with pytest.raises(ValidationError) as excinfo:
        arr_field.validate([1])
    assert "exact_items" not in excinfo.value.text
    assert "min_items" in excinfo.value.text


def test_array_exact_items_constraint():
    """Array with exact_items should enforce exact length."""
    arr_field = Array(items=IntField(), exact_items=3)
    # Valid input: list of three integers
    assert arr_field.validate([10, 20, 30]) == [10, 20, 30]
    # Invalid input: list of two integers
    with pytest.raises(ValidationError) as excinfo:
        arr_field.validate([10, 20])
    assert "exact_items" in excinfo.value.text
    # Invalid input: list of four integers
    with pytest.raises(ValidationError) as excinfo:
        arr_field.validate([10, 20, 30, 40])
    assert "exact_items" in excinfo.value.text


def test_array_unique_items_error():
    """Array with unique_items should reject duplicate elements."""
    arr_field = Array(items=IntField(), unique_items=True)
    # Valid input: unique integers
    assert arr_field.validate([1, 2, 3]) == [1, 2, 3]
    # Invalid input: duplicate integer
    with pytest.raises(ValidationError) as excinfo:
        arr_field.validate([1, 2, 1])
    # The error message should indicate a duplicate at the duplicate position
    messages = excinfo.value.messages()
    assert any(msg.code == "unique_items" for msg in messages)
    # Ensure the duplicate position is reported correctly
    duplicate_positions = [msg.key for msg in messages if msg.code == "unique_items"]
    assert duplicate_positions == [2]

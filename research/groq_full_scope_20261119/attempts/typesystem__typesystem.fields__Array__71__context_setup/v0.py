import pytest
from typesystem.fields import Array, Field
from typesystem.base import ValidationError


class IntField(Field):
    """Simple field that only accepts integers."""

    def validate(self, value):
        if not isinstance(value, int):
            raise self.validation_error("type")
        return value


def test_array_valid_min_and_max_items(tmp_path):
    """Array should accept a list of integers when min/max constraints are met."""
    arr_field = Array(items=IntField(), min_items=2, max_items=4)
    # Valid input: list of 3 integers
    result = arr_field.validate([1, 2, 3])
    assert result == [1, 2, 3]
    # Valid input: list of 2 integers (min boundary)
    result = arr_field.validate([10, 20])
    assert result == [10, 20]
    # Valid input: list of 4 integers (max boundary)
    result = arr_field.validate([5, 6, 7, 8])
    assert result == [5, 6, 7, 8]


def test_array_unique_items_error():
    """Array should raise ValidationError when duplicate items are present and unique_items=True."""
    arr_field = Array(items=IntField(), unique_items=True)
    with pytest.raises(ValidationError) as excinfo:
        arr_field.validate([1, 2, 1])
    errors = excinfo.value.messages()
    # Expect one error message for the duplicate at position 2
    assert len(errors) == 1
    assert errors[0].code == "unique_items"
    assert errors[0].key == 2
    assert "unique_items" in errors[0].text


def test_array_type_error_on_non_list_and_non_int_items():
    """Array should raise type errors for non-list input and for items that are not integers."""
    arr_field = Array(items=IntField())
    # Non-list input
    with pytest.raises(ValidationError) as excinfo:
        arr_field.validate("not a list")
    assert excinfo.value.messages()[0].code == "type"

    # List with a non-integer item
    with pytest.raises(ValidationError) as excinfo:
        arr_field.validate([1, "two", 3])
    errors = excinfo.value.messages()
    # Expect two errors: one for the string item and one for the duplicate check if any
    assert any(e.code == "type" for e in errors)
    # The error should point to the position of the string item
    assert any(e.key == 1 for e in errors)

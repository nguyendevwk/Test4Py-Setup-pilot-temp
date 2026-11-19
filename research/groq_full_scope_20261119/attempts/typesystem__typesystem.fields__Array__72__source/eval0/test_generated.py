import pytest
from typesystem import Array, String, Integer, ValidationError

def test_array_with_exact_items_and_unique():
    # Array expects exactly 3 items, all strings, and they must be unique
    field = Array(items=String(), exact_items=3, unique_items=True)
    # Valid input
    valid = ["a", "b", "c"]
    assert field.validate(valid) == ["a", "b", "c"]

    # Duplicate items should raise ValidationError
    with pytest.raises(ValidationError) as excinfo:
        field.validate(["x", "x", "y"])
    messages = excinfo.value.messages
    assert any(msg.code == "unique_items" for msg in messages)
    # The error should point to the duplicate position
    assert any(msg.key == 1 for msg in messages)

def test_array_with_additional_items_and_min_max():
    # Array expects at least 2 items, at most 4, first two must be integers, rest strings
    int_field = Integer()
    str_field = String()
    field = Array(items=[int_field, int_field], additional_items=str_field, min_items=2, max_items=4)
    # Valid input with 3 items
    valid = [1, 2, "three"]
    assert field.validate(valid) == [1, 2, "three"]

    # Too few items
    with pytest.raises(ValidationError) as excinfo:
        field.validate([1])
    assert excinfo.value.messages[0].code == "min_items"

    # Too many items
    with pytest.raises(ValidationError) as excinfo:
        field.validate([1, 2, "three", "four", "five"])
    assert excinfo.value.messages[0].code == "max_items"

    # Additional item not matching type
    with pytest.raises(ValidationError) as excinfo:
        field.validate([1, 2, 3])  # third item should be string
    assert excinfo.value.messages[0].code == "type"

def test_array_serialization_and_null_handling():
    # Array that allows null values
    field = Array(items=Integer(), allow_null=True)
    # Null should be returned as None
    assert field.validate(None) is None
    # Non-null list should be validated and serialized
    input_list = [1, 2, 3]
    validated = field.validate(input_list)
    assert validated == [1, 2, 3]
    # Serialization should preserve the list
    assert field.serialize(validated) == [1, 2, 3]
    # Serialization of None should return None
    assert field.serialize(None) is None

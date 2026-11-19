import pytest
from typesystem import ValidationError
from typesystem.fields import Array
from typesystem.fields import Integer


def test_array_validates_and_serializes_correctly():
    # Array of integers, no constraints
    field = Array(items=Integer())
    data = [1, 2, 3]
    # Validation should return the same list
    validated = field.validate(data)
    assert validated == [1, 2, 3]
    # Serialization should produce the same list
    serialized = field.serialize(validated)
    assert serialized == [1, 2, 3]


def test_array_min_max_and_exact_constraints():
    # Array must have exactly 2 items, each a string
    field = Array(items=Integer(), exact_items=2)
    # Too few items -> exact_items error
    with pytest.raises(ValidationError) as excinfo:
        field.validate([1])
    assert any(msg.code == "exact_items" for msg in excinfo.value.messages)

    # Too many items -> exact_items error
    with pytest.raises(ValidationError) as excinfo:
        field.validate([1, 2, 3])
    assert any(msg.code == "exact_items" for msg in excinfo.value.messages)

    # Correct number of items
    validated = field.validate([10, 20])
    assert validated == [10, 20]


def test_array_unique_items_error():
    # Array with unique items constraint
    field = Array(items=Integer(), unique_items=True)
    # Duplicate values should trigger unique_items error
    with pytest.raises(ValidationError) as excinfo:
        field.validate([1, 2, 1])
    messages = excinfo.value.messages
    assert any(msg.code == "unique_items" for msg in messages)
    # The error message should reference the duplicate position
    duplicate_positions = [msg.key for msg in messages if msg.code == "unique_items"]
    assert duplicate_positions == [2]

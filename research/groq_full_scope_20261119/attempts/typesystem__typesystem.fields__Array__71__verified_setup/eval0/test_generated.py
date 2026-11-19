import pytest
from typesystem import fields
from typesystem.exceptions import ValidationError

# Test 1: Normal validation with a list of integers and unique constraint
def test_array_normal_validation_and_uniqueness():
    # Array expects each element to be an integer
    int_field = fields.Integer()
    array_field = fields.Array(items=int_field, unique_items=True)

    # Valid input: all integers, no duplicates
    valid_input = [1, 2, 3]
    result = array_field.validate(valid_input)
    assert result == [1, 2, 3]

    # Invalid input: duplicate values should raise ValidationError
    duplicate_input = [1, 2, 1]
    with pytest.raises(ValidationError) as excinfo:
        array_field.validate(duplicate_input)
    # The error message should mention the duplicate position
    messages = excinfo.value.messages
    assert any(msg.code == "unique_items" for msg in messages)
    # The duplicate position should be the second occurrence (index 2)
    assert any(msg.key == 2 for msg in messages)

# Test 2: Boundary conditions for min_items and max_items
def test_array_min_max_boundary_conditions():
    # Array must have at least 2 items and at most 4 items
    array_field = fields.Array(min_items=2, max_items=4, items=fields.String())

    # Too few items: should raise ValidationError with 'min_items'
    too_few = ["a"]
    with pytest.raises(ValidationError) as excinfo_few:
        array_field.validate(too_few)
    assert any(msg.code == "min_items" for msg in excinfo_few.value.messages)

    # Too many items: should raise ValidationError with 'max_items'
    too_many = ["a", "b", "c", "d", "e"]
    with pytest.raises(ValidationError) as excinfo_many:
        array_field.validate(too_many)
    assert any(msg.code == "max_items" for msg in excinfo_many.value.messages)

    # Exactly within bounds: should pass
    within_bounds = ["x", "y", "z"]
    result = array_field.validate(within_bounds)
    assert result == ["x", "y", "z"]

# Test 3: Error handling for wrong type and null values
def test_array_type_and_null_errors():
    array_field = fields.Array(items=fields.Float(), allow_null=False)

    # Passing a non-list should raise 'type' error
    with pytest.raises(ValidationError) as excinfo_type:
        array_field.validate("not a list")
    assert any(msg.code == "type" for msg in excinfo_type.value.messages)

    # Passing None when nulls are not allowed should raise 'null' error
    with pytest.raises(ValidationError) as excinfo_null:
        array_field.validate(None)
    assert any(msg.code == "null" for msg in excinfo_null.value.messages)

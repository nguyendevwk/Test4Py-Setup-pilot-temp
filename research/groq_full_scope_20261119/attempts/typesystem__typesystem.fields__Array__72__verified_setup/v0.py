import pytest
from typesystem.fields import Array
from typesystem.base import ValidationError
from typesystem import fields

# Test 1: Normal validation with a homogeneous array of integers
def test_array_homogeneous_integers():
    arr_field = Array(items=fields.Integer())
    result = arr_field.validate([1, 2, 3])
    assert result == [1, 2, 3]  # values are unchanged
    # Ensure that the field accepts a single integer when min_items is 1
    single_result = arr_field.validate([42])
    assert single_result == [42]

# Test 2: Boundary conditions for min_items and max_items
def test_array_min_max_boundary():
    arr_field = Array(items=fields.String(), min_items=2, max_items=4)
    # Exactly at min boundary
    assert arr_field.validate(["a", "b"]) == ["a", "b"]
    # Exactly at max boundary
    assert arr_field.validate(["a", "b", "c", "d"]) == ["a", "b", "c", "d"]
    # Below min should raise ValidationError
    with pytest.raises(ValidationError) as excinfo:
        arr_field.validate(["only_one"])
    assert "Must have at least 2 items." in str(excinfo.value)
    # Above max should raise ValidationError
    with pytest.raises(ValidationError) as excinfo:
        arr_field.validate(["a", "b", "c", "d", "e"])
    assert "Must have no more than 4 items." in str(excinfo.value)

# Test 3: Unique items constraint
def test_array_unique_items():
    arr_field = Array(items=fields.Integer(), unique_items=True)
    # Valid unique array
    assert arr_field.validate([1, 2, 3]) == [1, 2, 3]
    # Duplicate should raise ValidationError with correct code
    with pytest.raises(ValidationError) as excinfo:
        arr_field.validate([1, 2, 1])
    errors = excinfo.value.messages
    assert any(err.code == "unique_items" for err in errors)
    # Ensure the error message mentions the duplicate position
    duplicate_error = next(err for err in errors if err.code == "unique_items")
    assert duplicate_error.key == 2  # duplicate at index 2

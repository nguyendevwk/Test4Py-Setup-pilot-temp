import decimal
import re
import typing
import pytest
from typesystem import fields, ValidationError

# Test 1: Successful validation with a matching child type
def test_union_validates_first_matching_child():
    union_field = fields.Union(any_of=[fields.Integer(), fields.String()])
    # Integer matches first child
    result = union_field.validate(42)
    assert result == 42
    # String matches second child
    result = union_field.validate("hello")
    assert result == "hello"

# Test 2: Null handling when allow_null is set via a child
def test_union_allows_null_when_child_allows():
    union_field = fields.Union(any_of=[fields.Integer(allow_null=True), fields.String()])
    # Null should be accepted
    result = union_field.validate(None)
    assert result is None
    # Non-null still validates correctly
    assert union_field.validate(10) == 10

# Test 3: ValidationError raised with correct message when no child matches
def test_union_raises_union_error_on_no_match():
    union_field = fields.Union(any_of=[fields.Integer(), fields.String()])
    with pytest.raises(ValidationError) as excinfo:
        union_field.validate(decimal.Decimal("3.14"))
    # The error should be the union error, not a type error from a child
    assert excinfo.value.code == "union"
    assert "Did not match any valid type." in str(excinfo.value)

import pytest
from typesystem import fields
from typesystem.base import ValidationError

def test_union_accepts_valid_type():
    union_field = fields.Union(any_of=[fields.Integer(), fields.String()])
    # Integer value should be accepted and returned unchanged
    assert union_field.validate(42) == 42
    # String value should be accepted and returned unchanged
    assert union_field.validate("hello") == "hello"

def test_union_null_behavior():
    # Union of Integer and String, neither allows null
    union_field = fields.Union(any_of=[fields.Integer(), fields.String()])
    with pytest.raises(ValidationError) as excinfo:
        union_field.validate(None)
    assert "null" in excinfo.value.messages()[0].code

    # Union where one child allows null
    string_allow_null = fields.String(allow_null=True)
    union_field_null = fields.Union(any_of=[fields.Integer(), string_allow_null])
    # Now None should be accepted
    assert union_field_null.validate(None) is None

def test_union_invalid_type_raises_union_error():
    union_field = fields.Union(any_of=[fields.Integer(), fields.String()])
    with pytest.raises(ValidationError) as excinfo:
        union_field.validate([1, 2, 3])  # list is not a valid type
    # The error should be the union error, not a type error from a child
    assert excinfo.value.messages()[0].code == "union"

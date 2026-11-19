import pytest
from typesystem import fields
from typesystem.base import ValidationError

def test_union_accepts_valid_type(tmp_path):
    # Union of Integer and String, no null allowed
    union_field = fields.Union([fields.Integer(), fields.String()])
    # Valid integer should pass
    assert union_field.validate(42) == 42
    # Valid string should pass
    assert union_field.validate("hello") == "hello"

def test_union_null_behavior(tmp_path):
    # Union with allow_null=True because one child allows null
    union_field = fields.Union([fields.Integer(allow_null=True), fields.String()])
    # Null should be accepted
    assert union_field.validate(None) is None
    # Union without allow_null should reject null
    union_no_null = fields.Union([fields.Integer(), fields.String()])
    with pytest.raises(ValidationError) as excinfo:
        union_no_null.validate(None)
    assert excinfo.value.code == "null"

def test_union_invalid_type_raises_union_error(tmp_path):
    # Union of Integer and String
    union_field = fields.Union([fields.Integer(), fields.String()])
    # Provide a value that matches neither type
    with pytest.raises(ValidationError) as excinfo:
        union_field.validate(3.14)  # float is neither int nor str
    # The error should be the union error
    assert excinfo.value.code == "union"
    # The error message should match the defined message
    assert str(excinfo.value) == "Did not match any valid type."

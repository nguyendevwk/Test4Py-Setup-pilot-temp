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
    # Non-null still validates against children
    assert union_field.validate(10) == 10
    assert union_field.validate("test") == "test"

# Test 3: ValidationError raised when no child matches and candidate errors exist
def test_union_raises_union_error_with_candidate_errors():
    # Child that accepts Decimal but raises a type error for int
    class DecimalField(fields.Decimal):
        def validate_or_error(self, value):
            try:
                return super().validate_or_error(value)
            except ValidationError as e:
                # Re-raise to propagate
                raise e

    union_field = fields.Union(any_of=[DecimalField(), fields.String()])
    # int does not match any child; DecimalField will produce a type error
    with pytest.raises(ValidationError) as excinfo:
        union_field.validate(5)
    # The raised error should be the union error, not the child type error
    assert excinfo.value.code == "union"
    assert "Did not match any valid type." in excinfo.value.message

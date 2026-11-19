import pytest
from typesystem.fields import Union
from typesystem.base import ValidationError

# Simple concrete Field implementations for testing
class IntField:
    errors = {"type": "Expected int."}

    def __init__(self, allow_null=False):
        self.allow_null = allow_null

    def validate(self, value):
        if value is None:
            if self.allow_null:
                return None
            raise ValidationError("Expected int.")
        if not isinstance(value, int):
            raise ValidationError("Expected int.")
        return value

class StrField:
    errors = {"type": "Expected str."}

    def __init__(self, allow_null=False):
        self.allow_null = allow_null

    def validate(self, value):
        if value is None:
            if self.allow_null:
                return None
            raise ValidationError("Expected str.")
        if not isinstance(value, str):
            raise ValidationError("Expected str.")
        return value

# Test 1: Successful validation with a matching child
def test_union_success_matching_child():
    union = Union(any_of=[IntField(), StrField()])
    assert union.validate(42) == 42
    assert union.validate("hello") == "hello"

# Test 2: Validation error when no child matches and exactly one candidate error
def test_union_error_single_candidate():
    union = Union(any_of=[IntField(), StrField()])
    with pytest.raises(ValidationError) as excinfo:
        union.validate(3.14)  # float does not match any child
    assert str(excinfo.value) == "Expected int." or str(excinfo.value) == "Expected str."

# Test 3: Null handling when allow_null is propagated from any child
def test_union_null_allowed():
    union = Union(any_of=[IntField(allow_null=True), StrField()])
    assert union.validate(None) is None
    # If no child allows null, validation should fail
    union_no_null = Union(any_of=[IntField(), StrField()])
    with pytest.raises(ValidationError) as excinfo:
        union_no_null.validate(None)
    assert str(excinfo.value) == "May not be null."

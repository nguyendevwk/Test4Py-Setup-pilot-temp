import pytest
from typesystem.fields import Union
from typesystem.base import ValidationError

# Simple concrete Field implementations for testing
class IntField(Union.__class__):  # inherit from Field
    errors = {"type": "Expected int."}

    def validate(self, value):
        if isinstance(value, int):
            return value
        raise self.validation_error("type")

class StrField(Union.__class__):
    errors = {"type": "Expected str."}

    def validate(self, value):
        if isinstance(value, str):
            return value
        raise self.validation_error("type")

def test_union_accepts_first_matching_type():
    """Union should return the value when the first child matches."""
    union = Union([IntField(), StrField()])
    result = union.validate(42)
    assert result == 42  # int matches first child

def test_union_returns_candidate_error_when_one_child_type_matches():
    """If only one child is of the correct type, its error should be raised."""
    union = Union([IntField(), StrField()])
    with pytest.raises(ValidationError) as excinfo:
        union.validate("not an int")
    # The error should come from IntField's type error
    assert excinfo.value.code == "type"
    assert "int" in excinfo.value.text

def test_union_raises_union_error_when_no_child_matches():
    """Union should raise its own error when no child validates."""
    union = Union([IntField(), StrField()])
    with pytest.raises(ValidationError) as excinfo:
        union.validate(3.14)  # float matches neither
    assert excinfo.value.code == "union"
    assert "Did not match any valid type." in excinfo.value.text

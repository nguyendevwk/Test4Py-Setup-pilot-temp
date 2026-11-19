import pytest
from typesystem.composites import Not
from typesystem.fields import Field

class EqualsField(Field):
    """A simple field that fails validation when the value equals a target."""
    def __init__(self, target, **kwargs):
        super().__init__(**kwargs)
        self.target = target

    def validate(self, value):
        if value == self.target:
            raise self.validation_error("equals")
        return value

def test_not_allows_non_matching_values():
    """Not should return the value when the negated field does not match."""
    negated = EqualsField(target=42)
    not_field = Not(negated)
    assert not_field.validate(10) == 10
    assert not_field.validate("hello") == "hello"
    assert not_field.validate(None) is None

def test_not_boundary_with_none_and_different_type():
    """Not should handle None and other types that do not match the negated field."""
    negated = EqualsField(target=0)
    not_field = Not(negated)
    # None is not equal to 0, so validation should pass
    assert not_field.validate(None) is None
    # A string that is not "0" should also pass
    assert not_field.validate("0") == "0"

def test_not_raises_when_negated_matches():
    """Not should raise a validation error when the negated field matches."""
    negated = EqualsField(target=99)
    not_field = Not(negated)
    with pytest.raises(Exception) as excinfo:
        not_field.validate(99)
    # The error message should come from Not.errors["negated"]
    assert "Must not match." in str(excinfo.value)

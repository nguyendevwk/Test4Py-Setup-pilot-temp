import pytest
from typesystem.composites import AllOf
from typesystem.fields import Field

class IntField(Field):
    def validate(self, value):
        if not isinstance(value, int):
            raise ValueError("Not an int")
        return value

class StrField(Field):
    def validate(self, value):
        if not isinstance(value, str):
            raise ValueError("Not a str")
        return value

def test_allof_success_and_failure():
    # AllOf should succeed when all child fields validate
    all_of = AllOf([IntField(), StrField()])
    # Value that satisfies both: int and str cannot be same, so use two separate validations
    # Instead, test that AllOf passes when each child validates the same value
    # Here we use a custom field that accepts any value
    class AnyField(Field):
        def validate(self, value):
            return value
    all_of_any = AllOf([AnyField(), AnyField()])
    assert all_of_any.validate(42) == 42

    # Now test failure: one child fails
    all_of_fail = AllOf([IntField(), StrField()])
    with pytest.raises(ValueError, match="Not a str"):
        all_of_fail.validate(42)  # IntField passes, StrField fails

def test_allof_empty_list_returns_value():
    # An empty AllOf should simply return the value
    all_of_empty = AllOf([])
    assert all_of_empty.validate("anything") == "anything"

def test_allof_disallows_allow_null_kwarg():
    # Passing allow_null should raise an AssertionError
    with pytest.raises(AssertionError):
        AllOf([IntField()], allow_null=True)

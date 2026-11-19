import pytest
import typesystem
from typesystem.schemas import Reference, ValidationError
from typesystem import Schema, fields


class Child(Schema):
    name = fields.String()


class Parent(Schema):
    child = Reference(to="child", definitions={"child": Child})


def test_reference_valid_object():
    """A valid child object is accepted and returned unchanged."""
    parent = Parent()
    child_obj = {"name": "Alice"}
    result = parent.child.validate(child_obj)
    assert isinstance(result, Child)
    assert result.name == "Alice"


def test_reference_allow_null():
    """When allow_null is True, None is accepted and returned unchanged."""
    class NullableParent(Schema):
        child = Reference(to="child", definitions={"child": Child}, allow_null=True)

    parent = NullableParent()
    result = parent.child.validate(None)
    assert result is None


def test_reference_invalid_value_raises():
    """Providing an invalid value raises ValidationError with correct message."""
    parent = Parent()
    with pytest.raises(ValidationError) as excinfo:
        parent.child.validate(123)  # not a dict
    assert "Invalid value" in str(excinfo.value)

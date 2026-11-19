import pytest
import typesystem
from typesystem.schemas import Reference, Definitions
from typesystem import ValidationError


class Child(typesystem.Schema):
    name = typesystem.String()


class Parent(typesystem.Schema):
    child = Reference(to="child", definitions=Definitions({"child": Child}))


def test_reference_validates_and_serializes():
    """Reference should validate a nested schema and serialize to a dict."""
    data = {"child": {"name": "Alice"}}
    parent = Parent(**data)
    assert isinstance(parent.child, Child)
    assert parent.child.name == "Alice"
    # serialization should produce a dict representation of the child
    assert parent.child.serialize() == {"name": "Alice"}


def test_reference_allows_null_when_configured():
    """Reference should allow None when allow_null is True."""
    class NullableParent(typesystem.Schema):
        child = Reference(
            to="child",
            definitions=Definitions({"child": Child}),
            allow_null=True,
        )

    parent = NullableParent(child=None)
    assert parent.child is None
    # serialization of None should remain None
    assert parent.child.serialize() is None


def test_reference_raises_validation_error_on_invalid_value():
    """Reference should raise ValidationError when value is not a dict."""
    with pytest.raises(ValidationError) as excinfo:
        Parent(child="not a dict")
    assert "child" in str(excinfo.value)
    assert "Expected a dict" in str(excinfo.value)

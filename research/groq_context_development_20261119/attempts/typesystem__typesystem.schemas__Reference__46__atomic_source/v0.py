import pytest
import typesystem
from typesystem.schemas import Reference
from typesystem import ValidationError
from typesystem.fields import Field


class NestedSchema(typesystem.Schema):
    name = typesystem.String()


class Definitions(dict):
    """Simple mapping that returns a schema class for a given key."""
    def __getitem__(self, key):
        return super().__getitem__(key)


class ParentSchema(typesystem.Schema):
    child = Reference(
        to="nested",
        definitions=Definitions({"nested": NestedSchema}),
        allow_null=False,
    )


class NullableParentSchema(typesystem.Schema):
    child = Reference(
        to="nested",
        definitions=Definitions({"nested": NestedSchema}),
        allow_null=True,
    )


def test_reference_valid_nested_object():
    """Reference should validate and return a NestedSchema instance."""
    data = {"child": {"name": "Alice"}}
    obj = ParentSchema.validate(data)
    assert isinstance(obj.child, NestedSchema)
    assert obj.child.name == "Alice"
    # serialization should produce a dict
    serialized = ParentSchema.serialize(obj)
    assert serialized == {"child": {"name": "Alice"}}


def test_reference_null_allowed():
    """Reference should allow None when allow_null is True."""
    data = {"child": None}
    obj = NullableParentSchema.validate(data)
    assert obj.child is None
    serialized = NullableParentSchema.serialize(obj)
    assert serialized == {"child": None}


def test_reference_invalid_value_raises():
    """Reference should raise ValidationError for invalid nested data."""
    data = {"child": {"name": 123}}  # name should be a string
    with pytest.raises(ValidationError) as excinfo:
        ParentSchema.validate(data)
    # The error message should mention the field name and the type mismatch
    assert "child" in str(excinfo.value)
    assert "String" in str(excinfo.value)

import pytest
from typesystem import Schema, ValidationError
from typesystem.schemas import Reference
from typesystem.fields import Field


class DummySchema(Schema):
    name = Field(str)


class ReferencingSchema(Schema):
    ref = Reference(to="dummy", definitions={"dummy": DummySchema})


def test_reference_validates_and_serializes_correctly():
    # Valid instance: non-null value that passes DummySchema validation
    data = {"ref": {"name": "Alice"}}
    obj = ReferencingSchema.validate(data)
    assert isinstance(obj, ReferencingSchema)
    assert obj.ref.name == "Alice"

    # Serialization should produce a dict representation of the nested schema
    serialized = ReferencingSchema.serialize(obj)
    assert serialized == {"ref": {"name": "Alice"}}


def test_reference_allows_null_when_allowed():
    # Allow null on the field
    class NullableSchema(Schema):
        ref = Reference(
            to="dummy",
            definitions={"dummy": DummySchema},
            allow_null=True,
        )

    data = {"ref": None}
    obj = NullableSchema.validate(data)
    assert obj.ref is None

    serialized = NullableSchema.serialize(obj)
    assert serialized == {"ref": None}


def test_reference_raises_validation_error_on_null_and_invalid_value():
    # Null not allowed
    with pytest.raises(ValidationError) as excinfo:
        ReferencingSchema.validate({"ref": None})
    assert "May not be null." in str(excinfo.value)

    # Invalid nested value
    with pytest.raises(ValidationError) as excinfo:
        ReferencingSchema.validate({"ref": {"name": 123}})
    assert "Invalid type" in str(excinfo.value)

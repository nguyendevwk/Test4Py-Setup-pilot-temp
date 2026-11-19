import pytest
import typesystem
from typesystem.schemas import Reference
from typesystem.base import ValidationError
from typesystem.schemas import Definitions
from typesystem import Schema, fields


class TargetSchema(Schema):
    name = fields.String()


class ContainerSchema(Schema):
    ref = Reference(to="Target", definitions=Definitions({"Target": TargetSchema}))


def test_reference_valid_object():
    """A valid object is validated and serialized correctly."""
    data = {"name": "Alice"}
    # Validate the nested object
    validated = ContainerSchema.ref.validate(data)
    assert isinstance(validated, TargetSchema)
    assert validated.name == "Alice"

    # Serialize the validated object
    serialized = ContainerSchema.ref.serialize(validated)
    assert serialized == {"name": "Alice"}


def test_reference_null_allowed():
    """When allow_null is True, None is accepted and returned unchanged."""
    # Create a Reference that allows null
    ref = Reference(
        to="Target",
        definitions=Definitions({"Target": TargetSchema}),
        allow_null=True,
    )
    # Validate None
    result = ref.validate(None)
    assert result is None

    # Serialize None
    serialized = ref.serialize(None)
    assert serialized is None


def test_reference_invalid_value_raises():
    """Providing an invalid value raises ValidationError with correct message."""
    with pytest.raises(ValidationError) as excinfo:
        ContainerSchema.ref.validate(123)  # int is not a dict
    # The error message should contain the field name and the target schema name
    assert "Target" in str(excinfo.value)
    assert "dict" in str(excinfo.value)

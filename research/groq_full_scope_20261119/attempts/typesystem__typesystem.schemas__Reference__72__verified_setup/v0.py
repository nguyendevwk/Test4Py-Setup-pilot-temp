import pytest
from typesystem import ValidationError
from typesystem.schemas import Reference, Definitions
from typesystem import Schema, Integer, String


class SimpleSchema(Schema):
    id = Integer()
    name = String()


def test_reference_valid_value(tmp_path):
    defs = Definitions({"simple": SimpleSchema})
    ref = Reference(to="simple", definitions=defs)
    # Valid instance
    data = {"id": 1, "name": "Alice"}
    validated = ref.validate(data)
    assert isinstance(validated, SimpleSchema)
    assert validated.id == 1
    assert validated.name == "Alice"
    # Serialization returns dict
    serialized = ref.serialize(validated)
    assert serialized == data


def test_reference_allow_null(tmp_path):
    defs = Definitions({"simple": SimpleSchema})
    ref = Reference(to="simple", definitions=defs, allow_null=True)
    # None is allowed
    assert ref.validate(None) is None
    # Serialization of None returns None
    assert ref.serialize(None) is None


def test_reference_invalid_value(tmp_path):
    defs = Definitions({"simple": SimpleSchema})
    ref = Reference(to="simple", definitions=defs)
    # Passing wrong type should raise ValidationError
    with pytest.raises(ValidationError) as excinfo:
        ref.validate({"id": "not-an-int", "name": "Bob"})
    assert "id" in str(excinfo.value)

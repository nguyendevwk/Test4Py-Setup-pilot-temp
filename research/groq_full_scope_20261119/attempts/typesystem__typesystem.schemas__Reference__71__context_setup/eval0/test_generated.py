import pytest
from typesystem import Schema, Integer, ValidationError
from typesystem.schemas import Reference, Definitions


class SimpleSchema(Schema):
    value = Integer()


def test_reference_validates_and_serializes_correctly():
    defs = Definitions({"simple": SimpleSchema})
    ref = Reference(to="simple", definitions=defs)
    # Validate a valid instance
    obj = ref.validate({"value": 42})
    assert isinstance(obj, SimpleSchema)
    assert obj.value == 42
    # Serialize the instance
    serialized = ref.serialize(obj)
    assert serialized == {"value": 42}


def test_reference_allows_null_when_configured():
    defs = Definitions({"simple": SimpleSchema})
    ref = Reference(to="simple", definitions=defs, allow_null=True)
    # Validate None when allow_null is True
    result = ref.validate(None)
    assert result is None
    # Serialization of None should also be None
    assert ref.serialize(None) is None


def test_reference_raises_error_when_null_not_allowed():
    defs = Definitions({"simple": SimpleSchema})
    ref = Reference(to="simple", definitions=defs, allow_null=False)
    with pytest.raises(ValidationError) as excinfo:
        ref.validate(None)
    assert "May not be null." in str(excinfo.value)

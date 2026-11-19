import pytest
from typesystem import Schema, ValidationError
from typesystem.schemas import Reference, Definitions


class SimpleSchema(Schema):
    name = Schema.String()


def test_reference_validates_and_serializes_correctly(tmp_path):
    defs = Definitions({"simple": SimpleSchema})
    ref_field = Reference(to="simple", definitions=defs, allow_null=False)

    # Valid value should pass validation and serialize to dict
    obj = SimpleSchema(name="Alice")
    validated = ref_field.validate(obj)
    assert validated is obj
    serialized = ref_field.serialize(obj)
    assert serialized == {"name": "Alice"}


def test_reference_raises_error_on_null_when_not_allowed():
    defs = Definitions({"simple": SimpleSchema})
    ref_field = Reference(to="simple", definitions=defs, allow_null=False)

    with pytest.raises(ValidationError) as excinfo:
        ref_field.validate(None)
    assert "May not be null." in str(excinfo.value)


def test_reference_allows_null_and_returns_none(tmp_path):
    defs = Definitions({"simple": SimpleSchema})
    ref_field = Reference(to="simple", definitions=defs, allow_null=True)

    # None should be accepted and returned unchanged
    result = ref_field.validate(None)
    assert result is None
    # Serialization of None should also be None
    assert ref_field.serialize(None) is None

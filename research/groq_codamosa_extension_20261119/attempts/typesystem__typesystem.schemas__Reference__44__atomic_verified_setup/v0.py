import pytest
import typesystem
from typesystem.schemas import Reference, ValidationError
from typesystem import Schema, String, Integer, Boolean, List, Dict


class TargetSchema(Schema):
    name = String()
    age = Integer()


class Definitions(dict):
    """Simple mapping that mimics typesystem's Definitions."""
    def __getitem__(self, key):
        return super().__getitem__(key)


def test_reference_valid_value():
    defs = Definitions({"target": TargetSchema})
    ref_field = Reference(to="target", definitions=defs)
    # Valid value: a dict matching TargetSchema
    valid_value = {"name": "Alice", "age": 30}
    validated = ref_field.validate(valid_value)
    # The returned object should be an instance of TargetSchema
    assert isinstance(validated, TargetSchema)
    assert validated.name == "Alice"
    assert validated.age == 30
    # Serialization should produce a plain dict
    serialized = ref_field.serialize(validated)
    assert serialized == {"name": "Alice", "age": 30}


def test_reference_allow_null():
    defs = Definitions({"target": TargetSchema})
    ref_field = Reference(to="target", definitions=defs, allow_null=True)
    # When allow_null is True, None should be accepted
    assert ref_field.validate(None) is None
    # Serialization of None should also be None
    assert ref_field.serialize(None) is None


def test_reference_invalid_value():
    defs = Definitions({"target": TargetSchema})
    ref_field = Reference(to="target", definitions=defs)
    # Passing a value that does not match TargetSchema should raise ValidationError
    invalid_value = {"name": "Bob", "age": "not-an-integer"}
    with pytest.raises(ValidationError) as excinfo:
        ref_field.validate(invalid_value)
    # The error message should contain the field name that failed
    assert "age" in str(excinfo.value)

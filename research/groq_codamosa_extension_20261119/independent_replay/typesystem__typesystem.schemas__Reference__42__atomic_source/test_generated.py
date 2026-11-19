import pytest
from typesystem.schemas import Reference
from typesystem.base import ValidationError

# Minimal mock of a schema that simply returns the value it receives
class DummySchema:
    def validate(self, value):
        return value

# Minimal mock of Definitions that behaves like a dict
class DummyDefinitions(dict):
    def __getitem__(self, key):
        return super().__getitem__(key)

def test_reference_validates_and_serializes_properly(tmp_path):
    # Arrange
    definitions = DummyDefinitions()
    dummy_schema = DummySchema()
    definitions["Dummy"] = dummy_schema
    ref_field = Reference(to="Dummy", definitions=definitions, allow_null=False)

    # Act
    validated = ref_field.validate({"key": "value"})
    serialized = ref_field.serialize(validated)

    # Assert
    assert validated == {"key": "value"}
    assert serialized == {"key": "value"}

def test_reference_allows_null_when_configured(tmp_path):
    # Arrange
    definitions = DummyDefinitions()
    dummy_schema = DummySchema()
    definitions["Dummy"] = dummy_schema
    ref_field = Reference(to="Dummy", definitions=definitions, allow_null=True)

    # Act
    validated = ref_field.validate(None)
    serialized = ref_field.serialize(validated)

    # Assert
    assert validated is None
    assert serialized is None

def test_reference_raises_error_on_null_when_not_allowed(tmp_path):
    # Arrange
    definitions = DummyDefinitions()
    dummy_schema = DummySchema()
    definitions["Dummy"] = dummy_schema
    ref_field = Reference(to="Dummy", definitions=definitions, allow_null=False)

    # Act & Assert
    with pytest.raises(ValidationError) as excinfo:
        ref_field.validate(None)
    assert "May not be null." in str(excinfo.value)

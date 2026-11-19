import pytest
from typesystem.schemas import Reference
from typesystem.base import ValidationError

class DummySchema:
    """A minimal schema that accepts any dict and returns it unchanged."""
    def validate(self, value):
        if not isinstance(value, dict):
            raise ValidationError("Expected dict")
        return value

class DummyDefinitions(dict):
    """A simple mapping that returns a DummySchema for a given key."""
    def __getitem__(self, key):
        return DummySchema()

def test_reference_validates_and_serializes_dict():
    defs = DummyDefinitions()
    ref = Reference(to="dummy", definitions=defs)
    input_value = {"key": "value"}
    # validate should return the same dict
    validated = ref.validate(input_value)
    assert validated is input_value
    # serialize should convert the dict to a plain dict (identity here)
    serialized = ref.serialize(validated)
    assert serialized == {"key": "value"}

def test_reference_allows_null_when_allowed():
    defs = DummyDefinitions()
    ref = Reference(to="dummy", definitions=defs, allow_null=True)
    # validate should return None when value is None and allow_null is True
    assert ref.validate(None) is None
    # serialize should also return None for a None input
    assert ref.serialize(None) is None

def test_reference_raises_on_null_when_not_allowed():
    defs = DummyDefinitions()
    ref = Reference(to="dummy", definitions=defs, allow_null=False)
    with pytest.raises(ValidationError) as excinfo:
        ref.validate(None)
    assert "May not be null." in str(excinfo.value)

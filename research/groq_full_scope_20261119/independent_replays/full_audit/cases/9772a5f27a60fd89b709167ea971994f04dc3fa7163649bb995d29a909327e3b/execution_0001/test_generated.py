import pytest
from typesystem.schemas import Reference, Definitions
from typesystem.base import ValidationError

class DummyTarget:
    """A minimal target that simply returns the value it receives."""
    def validate(self, value):
        return value

def test_reference_validates_and_serializes():
    defs = Definitions({"item": DummyTarget()})
    ref = Reference(to="item", definitions=defs)
    # Validate a normal value
    result = ref.validate({"key": "value"})
    assert result == {"key": "value"}
    # Serialize the validated object
    serialized = ref.serialize(result)
    assert serialized == {"key": "value"}

def test_reference_allows_null_when_allowed():
    defs = Definitions({"item": DummyTarget()})
    ref = Reference(to="item", definitions=defs, allow_null=True)
    # When allow_null is True, None should be accepted
    assert ref.validate(None) is None
    # Serializing None should also return None
    assert ref.serialize(None) is None

def test_reference_rejects_null_when_not_allowed():
    defs = Definitions({"item": DummyTarget()})
    ref = Reference(to="item", definitions=defs, allow_null=False)
    # When allow_null is False, None should raise ValidationError
    with pytest.raises(ValidationError) as excinfo:
        ref.validate(None)
    assert "May not be null." in str(excinfo.value)

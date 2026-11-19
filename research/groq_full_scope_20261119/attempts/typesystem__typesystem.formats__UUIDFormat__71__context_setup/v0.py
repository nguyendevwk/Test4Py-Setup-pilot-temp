import uuid
import pytest
from typesystem.formats import UUIDFormat
from typesystem.base import ValidationError

def test_uuidformat_valid_uuid_string():
    """Valid UUID string should be parsed into a uuid.UUID instance."""
    fmt = UUIDFormat()
    sample = "123e4567-e89b-12d3-a456-426614174000"
    result = fmt.validate(sample)
    assert isinstance(result, uuid.UUID)
    assert str(result) == sample

def test_uuidformat_invalid_uuid_raises():
    """Invalid UUID string should raise ValidationError with correct code."""
    fmt = UUIDFormat()
    invalid = "not-a-valid-uuid"
    with pytest.raises(ValidationError) as excinfo:
        fmt.validate(invalid)
    assert excinfo.value.code == "format"
    assert "Must be a valid UUID format." in str(excinfo.value)

def test_uuidformat_serialize_and_none():
    """serialize should return string representation or None."""
    fmt = UUIDFormat()
    u = uuid.UUID("123e4567-e89b-12d3-a456-426614174000")
    assert fmt.serialize(u) == "123e4567-e89b-12d3-a456-426614174000"
    assert fmt.serialize(None) is None

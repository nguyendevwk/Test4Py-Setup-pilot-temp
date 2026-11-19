import uuid
import pytest
from typesystem.formats import UUIDFormat
from typesystem.base import ValidationError

def test_uuidformat_valid_uuid_string():
    fmt = UUIDFormat()
    # A canonical UUID string
    uuid_str = "123e4567-e89b-12d3-a456-426614174000"
    result = fmt.validate(uuid_str)
    assert isinstance(result, uuid.UUID)
    assert str(result) == uuid_str

def test_uuidformat_serialize_none_and_uuid():
    fmt = UUIDFormat()
    # Serializing None should return None
    assert fmt.serialize(None) is None
    # Serializing a UUID instance should return its string representation
    u = uuid.UUID("123e4567-e89b-12d3-a456-426614174000")
    assert fmt.serialize(u) == "123e4567-e89b-12d3-a456-426614174000"

def test_uuidformat_invalid_string_raises():
    fmt = UUIDFormat()
    # An invalid UUID string should raise ValidationError
    with pytest.raises(ValidationError) as excinfo:
        fmt.validate("not-a-uuid")
    assert "Must be a valid UUID format." in str(excinfo.value)

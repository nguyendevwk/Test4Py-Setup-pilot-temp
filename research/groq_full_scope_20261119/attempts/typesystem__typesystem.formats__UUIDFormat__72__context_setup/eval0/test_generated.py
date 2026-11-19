import uuid
import pytest
from typesystem.formats import UUIDFormat
from typesystem.base import ValidationError

def test_validate_success_and_serialize():
    fmt = UUIDFormat()
    # A canonical UUID string
    uuid_str = "123e4567-e89b-12d3-a456-426614174000"
    # Validate should return a uuid.UUID instance
    result = fmt.validate(uuid_str)
    assert isinstance(result, uuid.UUID)
    assert str(result) == uuid_str
    # Serialize should return the string representation
    serialized = fmt.serialize(result)
    assert serialized == uuid_str
    # Serializing None should return None
    assert fmt.serialize(None) is None

def test_validate_invalid_format_raises():
    fmt = UUIDFormat()
    # A string that does not match UUID regex
    invalid_str = "not-a-uuid"
    with pytest.raises(ValidationError) as excinfo:
        fmt.validate(invalid_str)
    # The error message should match the defined format error
    assert str(excinfo.value) == "Must be a valid UUID format."
    assert excinfo.value.code == "format"

def test_is_native_type_and_serialize_with_uuid_object():
    fmt = UUIDFormat()
    # Create a UUID object directly
    u = uuid.UUID("123e4567-e89b-12d3-a456-426614174000")
    # is_native_type should recognize it
    assert fmt.is_native_type(u) is True
    # serialize should work without raising
    assert fmt.serialize(u) == str(u)

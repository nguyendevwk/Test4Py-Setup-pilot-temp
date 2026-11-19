import uuid
import pytest
from typesystem.formats import UUIDFormat

# Test normal behavior: a valid UUID string is parsed correctly
def test_uuidformat_valid_uuid():
    fmt = UUIDFormat()
    valid_str = "12345678-1234-5678-1234-567812345678"
    result = fmt.validate(valid_str)
    assert isinstance(result, uuid.UUID)
    assert str(result) == valid_str

# Test boundary behavior: serializing None returns None
def test_uuidformat_serialize_none():
    fmt = UUIDFormat()
    assert fmt.serialize(None) is None

# Test error behavior: an invalid UUID string raises ValidationError
def test_uuidformat_invalid_uuid():
    fmt = UUIDFormat()
    invalid_str = "not-a-uuid"
    with pytest.raises(Exception) as excinfo:
        fmt.validate(invalid_str)
    # The exception should be a ValidationError from typesystem.base
    from typesystem.base import ValidationError
    assert isinstance(excinfo.value, ValidationError)
    assert "Must be a valid UUID format." in str(excinfo.value)

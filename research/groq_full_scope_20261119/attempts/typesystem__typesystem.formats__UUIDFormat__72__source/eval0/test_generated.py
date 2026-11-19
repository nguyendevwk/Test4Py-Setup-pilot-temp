import uuid
import pytest
from typesystem.formats import UUIDFormat

# Test 1: Valid UUID string is correctly parsed and returned as a uuid.UUID instance
def test_uuidformat_valid_uuid():
    fmt = UUIDFormat()
    valid_str = "123e4567-e89b-12d3-a456-426614174000"
    result = fmt.validate(valid_str)
    assert isinstance(result, uuid.UUID)
    assert str(result) == valid_str

# Test 2: Invalid UUID string raises ValidationError with correct message
def test_uuidformat_invalid_uuid():
    fmt = UUIDFormat()
    invalid_str = "not-a-uuid"
    with pytest.raises(Exception) as excinfo:
        fmt.validate(invalid_str)
    # The exception should be a ValidationError from typesystem.base
    from typesystem.base import ValidationError
    assert isinstance(excinfo.value, ValidationError)
    assert "Must be a valid UUID format." in str(excinfo.value)

# Test 3: Serializing a uuid.UUID instance returns its string representation,
# and serializing None returns None
def test_uuidformat_serialize():
    fmt = UUIDFormat()
    u = uuid.UUID("123e4567-e89b-12d3-a456-426614174000")
    assert fmt.serialize(u) == "123e4567-e89b-12d3-a456-426614174000"
    assert fmt.serialize(None) is None

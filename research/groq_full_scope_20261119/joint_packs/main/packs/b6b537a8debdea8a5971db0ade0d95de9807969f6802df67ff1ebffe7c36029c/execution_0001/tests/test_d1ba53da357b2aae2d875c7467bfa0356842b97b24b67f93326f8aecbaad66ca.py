import uuid
import pytest
from typesystem.formats import UUIDFormat

# Test 1: validate accepts a correct UUID string and returns a uuid.UUID instance
def test_uuidformat_validate_success():
    fmt = UUIDFormat()
    valid_str = "123e4567-e89b-12d3-a456-426614174000"
    result = fmt.validate(valid_str)
    assert isinstance(result, uuid.UUID)
    assert str(result) == valid_str

# Test 2: validate raises ValidationError for an invalid UUID string
def test_uuidformat_validate_failure():
    fmt = UUIDFormat()
    invalid_str = "not-a-uuid"
    with pytest.raises(Exception) as excinfo:
        fmt.validate(invalid_str)
    # The exception should be a ValidationError from typesystem.base
    from typesystem.base import ValidationError
    assert isinstance(excinfo.value, ValidationError)
    assert "Must be a valid UUID format." in str(excinfo.value)

# Test 3: serialize correctly handles None and uuid.UUID objects
def test_uuidformat_serialize():
    fmt = UUIDFormat()
    # None should serialize to None
    assert fmt.serialize(None) is None
    # A uuid.UUID instance should serialize to its string representation
    u = uuid.UUID("123e4567-e89b-12d3-a456-426614174000")
    assert fmt.serialize(u) == "123e4567-e89b-12d3-a456-426614174000"
    # Passing a non-UUID should raise an AssertionError
    with pytest.raises(AssertionError):
        fmt.serialize("not-a-uuid")

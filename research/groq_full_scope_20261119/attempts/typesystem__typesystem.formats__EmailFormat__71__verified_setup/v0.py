import pytest
from typesystem.formats import EmailFormat

# Test that a valid email passes validation and returns the same string
def test_email_format_valid():
    fmt = EmailFormat()
    valid_email = "user@example.com"
    result = fmt.validate(valid_email)
    assert result == valid_email

# Test that an invalid email raises a ValidationError with the correct message
def test_email_format_invalid():
    fmt = EmailFormat()
    invalid_email = "not-an-email"
    with pytest.raises(Exception) as excinfo:
        fmt.validate(invalid_email)
    # The exception should be a ValidationError from typesystem.base
    from typesystem.base import ValidationError
    assert isinstance(excinfo.value, ValidationError)
    assert str(excinfo.value) == fmt.errors["format"]

# Test that serializing None returns None
def test_email_format_serialize_none(tmp_path):
    fmt = EmailFormat()
    assert fmt.serialize(None) is None

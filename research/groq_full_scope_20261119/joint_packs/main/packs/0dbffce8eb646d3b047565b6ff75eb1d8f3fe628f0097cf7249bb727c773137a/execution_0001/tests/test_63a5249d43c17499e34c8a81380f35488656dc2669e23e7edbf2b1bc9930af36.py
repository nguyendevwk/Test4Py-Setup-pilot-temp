import pytest
from typesystem.formats import EmailFormat
from typesystem.base import ValidationError

def test_valid_email_passes_validation():
    fmt = EmailFormat()
    valid_email = "user.name+tag@example.com"
    result = fmt.validate(valid_email)
    assert result == valid_email

def test_invalid_email_raises_validation_error():
    fmt = EmailFormat()
    invalid_email = "not-an-email"
    with pytest.raises(ValidationError) as excinfo:
        fmt.validate(invalid_email)
    assert str(excinfo.value) == fmt.errors["format"]

def test_serialize_none_returns_none():
    fmt = EmailFormat()
    assert fmt.serialize(None) is None

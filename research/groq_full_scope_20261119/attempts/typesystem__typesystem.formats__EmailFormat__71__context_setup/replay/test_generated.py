import pytest
from typesystem.formats import EmailFormat
from typesystem.base import ValidationError

def test_email_format_valid():
    fmt = EmailFormat()
    valid_email = "user.name+tag@example.co.uk"
    # validate should return the same string for a valid email
    assert fmt.validate(valid_email) == valid_email

def test_email_format_invalid():
    fmt = EmailFormat()
    invalid_email = "not-an-email"
    # validate should raise ValidationError for an invalid email
    with pytest.raises(ValidationError) as excinfo:
        fmt.validate(invalid_email)
    # The error message should match the defined format error
    assert str(excinfo.value) == "Must be a valid email format."

def test_email_format_serialize_none():
    fmt = EmailFormat()
    # serialize should return None when given None
    assert fmt.serialize(None) is None

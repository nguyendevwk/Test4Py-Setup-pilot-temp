import re
import pytest
from typesystem.formats import EmailFormat

# Helper: a simple regex that matches the same pattern used in the module
EMAIL_REGEX = re.compile(r"^[^@]+@[^@]+\.[^@]+$")

def test_email_format_valid():
    """EmailFormat should accept a correctly formatted email."""
    fmt = EmailFormat()
    valid_email = "user@example.com"
    # Validate returns the same string
    assert fmt.validate(valid_email) == valid_email
    # Serialize returns the same string
    assert fmt.serialize(valid_email) == valid_email

def test_email_format_invalid():
    """EmailFormat should raise ValidationError for malformed emails."""
    fmt = EmailFormat()
    invalid_email = "invalid-email"
    with pytest.raises(fmt.ValidationError):
        fmt.validate(invalid_email)

def test_email_format_serialize_none():
    """EmailFormat.serialize should return None when given None."""
    fmt = EmailFormat()
    assert fmt.serialize(None) is None

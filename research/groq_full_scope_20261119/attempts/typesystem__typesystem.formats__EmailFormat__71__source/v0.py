import re
import pytest
from typesystem.formats import EmailFormat

# Helper: a simple regex to check email format used by EmailFormat
# (the actual EMAIL_REGEX is imported from the module, but we replicate it here for clarity)
EMAIL_REGEX = re.compile(r"^[^@]+@[^@]+\.[^@]+$")

def test_email_format_valid():
    """EmailFormat should accept a correctly formatted email address."""
    fmt = EmailFormat()
    valid_email = "user@example.com"
    # Validate should return the same string
    assert fmt.validate(valid_email) == valid_email
    # Serialize should return the same string
    assert fmt.serialize(valid_email) == valid_email

def test_email_format_invalid():
    """EmailFormat should raise ValidationError for an invalid email address."""
    fmt = EmailFormat()
    invalid_email = "not-an-email"
    with pytest.raises(fmt.ValidationError):
        fmt.validate(invalid_email)

def test_email_format_serialize_none():
    """EmailFormat.serialize should return None when given None."""
    fmt = EmailFormat()
    assert fmt.serialize(None) is None

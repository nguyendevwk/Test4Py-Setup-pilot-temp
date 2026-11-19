import re
import pytest
from typesystem.formats import EmailFormat

# Helper to access the internal regex used by EmailFormat
# The regex is defined in the module as EMAIL_REGEX
EMAIL_REGEX = re.compile(r"^[^@]+@[^@]+\.[^@]+$")

def test_email_format_valid():
    """EmailFormat should accept a standard email address."""
    fmt = EmailFormat()
    valid_email = "user@example.com"
    # validate should return the same string for a valid email
    assert fmt.validate(valid_email) == valid_email
    # serialize should return the same string
    assert fmt.serialize(valid_email) == valid_email

def test_email_format_invalid():
    """EmailFormat should raise ValidationError for malformed emails."""
    fmt = EmailFormat()
    invalid_email = "not-an-email"
    with pytest.raises(Exception) as excinfo:
        fmt.validate(invalid_email)
    # The exception should be a ValidationError with the correct message
    assert hasattr(excinfo.value, "message")
    assert "Must be a valid email format." in str(excinfo.value)

def test_email_format_boundary_cases():
    """Test boundary conditions: empty string and None."""
    fmt = EmailFormat()
    # Empty string should be invalid
    with pytest.raises(Exception):
        fmt.validate("")
    # None should be handled by serialize but not by validate
    assert fmt.serialize(None) is None

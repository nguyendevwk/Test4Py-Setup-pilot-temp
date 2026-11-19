import pytest
from string_utils.validation import is_email

def test_is_email_valid_basic():
    """A simple, correctly formatted email should return True."""
    assert is_email("user@example.com") is True

def test_is_email_boundary_length():
    """An email with maximum allowed lengths (64 for local part, 255 for domain) should be accepted."""
    local = "a" * 64
    domain = "b" * 255
    email = f"{local}@{domain}"
    assert len(email) <= 320
    assert is_email(email) is True

def test_is_email_invalid_multiple_at_and_escaped():
    """An email containing multiple '@' signs where the first is escaped should be rejected."""
    # The first '@' is escaped, but the second is not, making the address invalid
    invalid_email = r"user\@example@domain.com"
    assert is_email(invalid_email) is False

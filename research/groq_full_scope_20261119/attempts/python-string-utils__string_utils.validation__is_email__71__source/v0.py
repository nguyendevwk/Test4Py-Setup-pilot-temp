import pytest
from string_utils.validation import is_email

def test_valid_email_basic():
    # Basic valid email should return True
    assert is_email("user@example.com") is True

def test_invalid_email_boundary():
    # Email exceeding maximum length or with invalid characters should return False
    long_local = "a" * 65  # exceeds 64 chars for local part
    long_domain = "b" * 256  # exceeds 255 chars for domain part
    assert is_email(f"{long_local}@example.com") is False
    assert is_email(f"user@{long_domain}") is False
    # Email starting with a dot or containing consecutive dots in local part
    assert is_email(".user@example.com") is False
    assert is_email("user..name@example.com") is False

def test_invalid_email_multiple_at_and_escaped():
    # Multiple '@' signs without proper escaping should be invalid
    assert is_email("user@@example.com") is False
    # Escaped '@' should be handled correctly
    assert is_email(r"user\@name@example.com") is True

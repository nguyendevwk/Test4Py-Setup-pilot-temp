import pytest
from string_utils.validation import is_email

def test_is_email_valid_basic():
    """Valid email should return True."""
    assert is_email("user@example.com") is True
    assert is_email("my.email@the-provider.com") is True

def test_is_email_boundary_and_invalid():
    """Boundary conditions: length limits, leading dot, consecutive dots, and escaped @."""
    # Too long local part (>64)
    long_local = "a" * 65 + "@example.com"
    assert is_email(long_local) is False

    # Too long domain part (>255)
    long_domain = "user@" + "b" * 256
    assert is_email(long_domain) is False

    # Leading dot in local part
    assert is_email(".user@example.com") is False

    # Consecutive dots in local part
    assert is_email("user..name@example.com") is False

    # Escaped @ sign inside local part
    assert is_email(r"user\@name@example.com") is True

def test_is_email_error_handling():
    """Emails with multiple @ signs without proper escaping should be False."""
    # Multiple @ without escaping
    assert is_email("user@@example.com") is False

    # Multiple @ with escaping only in domain part
    assert is_email("user@ex@ample.com") is False

    # Empty string and non-string input
    assert is_email("") is False
    assert is_email(123) is False

import pytest
from string_utils.validation import is_email

def test_is_email_valid_basic():
    """Valid email should return True."""
    assert is_email("user@example.com") is True
    assert is_email("my.email@the-provider.com") is True
    # quoted local part with spaces removed
    assert is_email('"user name"@example.com') is True

def test_is_email_boundary_length_and_format():
    """Emails at boundary lengths and with edge cases should be handled correctly."""
    # maximum allowed length 320
    local = "a" * 64
    domain = "b" * 255
    long_email = f"{local}@{domain}"
    assert len(long_email) <= 320
    assert is_email(long_email) is True

    # local part starting with dot or ending with dot should be invalid
    assert is_email(".user@example.com") is False
    assert is_email("user.@example.com") is False

    # consecutive dots in local part invalid
    assert is_email("user..name@example.com") is False

def test_is_email_invalid_cases():
    """Various invalid inputs should return False."""
    # empty string
    assert is_email("") is False

    # no @ symbol
    assert is_email("userexample.com") is False

    # multiple @ without escape
    assert is_email("user@@example.com") is False

    # escaped @ sign handled correctly
    assert is_email(r"user\@example.com") is True

    # local part too long
    assert is_email("a" * 65 + "@example.com") is False

    # domain part too long
    assert is_email("user@" + "b" * 256) is False

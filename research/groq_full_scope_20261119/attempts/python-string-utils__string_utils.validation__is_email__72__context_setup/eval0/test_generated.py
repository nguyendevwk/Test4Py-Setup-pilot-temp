import pytest
from string_utils.validation import is_email

def test_is_email_valid_and_invalid():
    # Valid email
    assert is_email('my.email@the-provider.com') is True
    # Invalid: starts with dot, missing local part, or too many @
    assert is_email('.john@doe.com') is False
    assert is_email('@gmail.com') is False
    assert is_email('john@@doe.com') is False

def test_is_email_boundary_lengths():
    # Local part max 64 chars, domain max 255 chars, total <= 320
    local = 'a' * 64
    domain = 'b' * 255
    assert len(local + '@' + domain) <= 320
    assert is_email(f'{local}@{domain}') is True

    # Exceed total length
    long_local = 'a' * 65
    long_domain = 'b' * 256
    assert len(long_local + '@' + long_domain) > 320
    assert is_email(f'{long_local}@{long_domain}') is False

def test_is_email_escaped_at_sign():
    # Email with escaped @ sign in local part
    assert is_email(r'john\@doe@example.com') is True
    # Unescaped multiple @ signs without escape
    assert is_email('john@@example.com') is False

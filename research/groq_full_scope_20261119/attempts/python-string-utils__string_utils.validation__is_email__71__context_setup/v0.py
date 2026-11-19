import pytest
from string_utils.validation import is_email

def test_is_email_valid_and_invalid():
    # Valid email
    assert is_email('my.email@the-provider.com') is True
    # Invalid: starts with dot
    assert is_email('.myemail@provider.com') is False
    # Invalid: missing local part
    assert is_email('@gmail.com') is False
    # Invalid: multiple consecutive dots in local part
    assert is_email('john..doe@example.com') is False
    # Invalid: local part too long
    long_local = 'a' * 65
    assert is_email(f'{long_local}@example.com') is False
    # Invalid: domain part too long
    long_domain = 'b' * 256
    assert is_email(f'user@{long_domain}') is False

def test_is_email_boundary_lengths():
    # Exactly 320 characters total
    local = 'a' * 64
    domain = 'b' * 255
    email = f'{local}@{domain}'
    assert len(email) == 320
    assert is_email(email) is True
    # One character over the limit
    email_over = f'{local}@{domain}c'
    assert len(email_over) == 321
    assert is_email(email_over) is False

def test_is_email_escaped_at_sign_and_quotes():
    # Escaped @ sign inside quotes should be treated as part of local part
    assert is_email('"john\\@doe"@example.com') is True
    # Escaped @ sign not inside quotes should be invalid
    assert is_email('john\\@doe@example.com') is False
    # Local part with escaped space
    assert is_email('john\\ doe@example.com') is True
    # Local part with leading/trailing quotes and spaces removed
    assert is_email('"  john doe  "@example.com') is True

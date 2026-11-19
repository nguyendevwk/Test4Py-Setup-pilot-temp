import pytest
from string_utils.validation import is_email

def test_is_email_various_cases():
    # Valid email
    assert is_email('user@example.com') is True

    # Invalid: empty string, non-string, or only spaces
    assert is_email('') is False
    assert is_email('   ') is False
    assert is_email(None) is False
    assert is_email(123) is False

    # Invalid: starts with dot, missing local part, or missing domain
    assert is_email('.user@example.com') is False
    assert is_email('@example.com') is False
    assert is_email('user@') is False

    # Invalid: head too long (>64), tail too long (>255)
    long_head = 'a' * 65
    long_tail = 'b' * 256
    assert is_email(f'{long_head}@example.com') is False
    assert is_email(f'user@{long_tail}') is False

    # Invalid: head ends with dot or contains consecutive dots
    assert is_email('user.@example.com') is False
    assert is_email('user..name@example.com') is False

    # Invalid: overall length >320
    long_email = 'a' * 321
    assert is_email(long_email) is False

    # Valid: escaped space in local part
    assert is_email('user\\ name@example.com') is True

    # Valid: quoted local part with spaces
    assert is_email('"user name"@example.com') is True

    # Valid: escaped @ in local part with multiple @ signs
    assert is_email('user\\@example@domain.com') is True

    # Invalid: multiple @ signs without escape
    assert is_email('user@example@domain.com') is False

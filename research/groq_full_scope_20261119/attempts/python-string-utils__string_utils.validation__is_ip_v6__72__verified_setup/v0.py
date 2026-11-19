import pytest
from string_utils.validation import is_ip_v6

def test_is_ip_v6_valid_address():
    """A correctly formatted IPv6 address should return True."""
    valid = "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
    assert is_ip_v6(valid) is True

def test_is_ip_v6_invalid_address():
    """An address with an illegal character should return False."""
    invalid = "2001:0db8:85a3:0000:0000:8a2e:0370:733g"  # 'g' is not a hex digit
    assert is_ip_v6(invalid) is False

def test_is_ip_v6_non_string_input():
    """Non‑string inputs should be treated as invalid and return False."""
    assert is_ip_v6(12345) is False
    assert is_ip_v6(None) is False

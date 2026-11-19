import pytest
from string_utils.validation import is_ip_v6

def test_is_ip_v6_valid_ipv6_address():
    """A correctly formatted IPv6 address should return True."""
    ipv6 = "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
    assert is_ip_v6(ipv6) is True

def test_is_ip_v6_invalid_characters():
    """An IPv6 address containing invalid characters should return False."""
    invalid_ipv6 = "2001:db8:85a3:0000:0000:8a2e:370:?7334"
    assert is_ip_v6(invalid_ipv6) is False

def test_is_ip_v6_non_string_input():
    """Non-string inputs should be treated as invalid and return False."""
    assert is_ip_v6(12345) is False
    assert is_ip_v6(None) is False
    assert is_ip_v6(["2001::1"]) is False

import pytest
from string_utils.validation import is_ip_v4

def test_valid_ip_address():
    """A correctly formatted IPv4 address should return True."""
    assert is_ip_v4("192.168.0.1") is True
    assert is_ip_v4("0.0.0.0") is True
    assert is_ip_v4("255.255.255.255") is True

def test_invalid_ip_address_boundary():
    """IP octets outside 0-255 or malformed strings should return False."""
    # Octet too large
    assert is_ip_v4("256.100.50.25") is False
    # Negative number
    assert is_ip_v4("-1.100.50.25") is False
    # Too many octets
    assert is_ip_v4("1.2.3.4.5") is False
    # Missing octet
    assert is_ip_v4("1.2.3") is False
    # Non-numeric characters
    assert is_ip_v4("abc.def.ghi.jkl") is False

def test_non_string_input():
    """Non-string inputs should be treated as invalid and return False."""
    assert is_ip_v4(12345) is False
    assert is_ip_v4(None) is False
    assert is_ip_v4(["192", "168", "0", "1"]) is False

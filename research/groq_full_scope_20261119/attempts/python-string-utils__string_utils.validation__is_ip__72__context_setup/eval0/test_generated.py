import pytest
from string_utils.validation import is_ip

def test_is_ip_valid_ipv4():
    """Valid IPv4 addresses should return True."""
    assert is_ip("192.168.0.1") is True
    assert is_ip("0.0.0.0") is True
    assert is_ip("255.255.255.255") is True

def test_is_ip_valid_ipv6():
    """Valid IPv6 addresses should return True."""
    assert is_ip("2001:0db8:85a3:0000:0000:8a2e:0370:7334") is True
    assert is_ip("::1") is True
    assert is_ip("fe80::") is True

def test_is_ip_invalid_inputs():
    """Invalid inputs should return False."""
    assert is_ip("256.100.50.25") is False          # octet out of range
    assert is_ip("123.456.78.90") is False          # octet out of range
    assert is_ip("2001:db8:85a3::8a2e:370:7334:") is False  # trailing colon
    assert is_ip("not an ip") is False
    assert is_ip("") is False
    assert is_ip(None) is False

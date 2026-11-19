import pytest
from string_utils.validation import is_ip_v4

def test_valid_ipv4_address():
    """A correctly formatted IPv4 address should return True."""
    assert is_ip_v4("192.168.0.1") is True
    assert is_ip_v4("0.0.0.0") is True
    assert is_ip_v4("255.255.255.255") is True

def test_invalid_ipv4_address_out_of_range():
    """An address with a segment outside 0-255 should return False."""
    assert is_ip_v4("256.100.50.25") is False
    assert is_ip_v4("192.168.1.256") is False
    assert is_ip_v4("10.0.0.-1") is False

def test_non_string_input_returns_false():
    """Non‑string inputs should be rejected and return False."""
    assert is_ip_v4(12345) is False
    assert is_ip_v4(None) is False
    assert is_ip_v4(["192.168.0.1"]) is False

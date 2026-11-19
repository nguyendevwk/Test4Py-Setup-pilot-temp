import pytest
from string_utils.validation import is_ip_v6

def test_valid_ipv6_full_address():
    """A fully expanded IPv6 address should be accepted."""
    addr = "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
    assert is_ip_v6(addr) is True

def test_invalid_ipv6_due_to_non_hex_character():
    """An address containing a non-hex character should be rejected."""
    addr = "2001:0db8:85a3:0000:0000:8a2e:0370:zzzz"
    assert is_ip_v6(addr) is False

def test_non_string_input_returns_false():
    """Non-string inputs should be considered invalid IPv6 addresses."""
    assert is_ip_v6(12345) is False
    assert is_ip_v6(None) is False
    assert is_ip_v6(["2001::1"]) is False

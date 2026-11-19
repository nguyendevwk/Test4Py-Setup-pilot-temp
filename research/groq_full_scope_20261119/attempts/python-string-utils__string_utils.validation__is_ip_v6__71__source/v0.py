import pytest
from string_utils.validation import is_ip_v6

def test_valid_ipv6_full_address():
    """A fully expanded IPv6 address should be recognized as valid."""
    addr = "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
    assert is_ip_v6(addr) is True

def test_invalid_ipv6_with_non_hex_character():
    """An IPv6 address containing an invalid character should be rejected."""
    addr = "2001:0db8:85a3:0000:0000:8a2e:0370:zzzz"
    assert is_ip_v6(addr) is False

def test_non_string_input_returns_false():
    """Non‑string inputs should not be considered valid IPv6 addresses."""
    assert is_ip_v6(12345) is False
    assert is_ip_v6(None) is False

import pytest
from string_utils.validation import is_ip_v6

def test_valid_ipv6_address():
    # A canonical IPv6 address should be recognized as valid.
    addr = "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
    assert is_ip_v6(addr) is True

def test_invalid_ipv6_address_with_invalid_char():
    # An address containing an invalid character should be rejected.
    addr = "2001:0db8:85a3:0000:0000:8a2e:0370:733?"
    assert is_ip_v6(addr) is False

def test_non_string_input_returns_false():
    # Passing a non-string (e.g., None) should not raise an exception and return False.
    assert is_ip_v6(None) is False

import pytest
from sanic.headers import fwd_normalize_address
from sanic.exceptions import InvalidHeader

def test_normal_lowercase_and_bracket_ipv6():
    # Normal IPv4-like address should be lowercased
    assert fwd_normalize_address("192.168.1.1") == "192.168.1.1"
    # IPv6 address should be bracketed and lowercased
    ipv6 = "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
    assert fwd_normalize_address(ipv6) == f"[{ipv6.lower()}]"

def test_unknown_raises_value_error():
    # The string "unknown" must raise ValueError
    with pytest.raises(ValueError):
        fwd_normalize_address("unknown")

def test_obfuscated_prefix_retains_case():
    # Addresses starting with underscore should not be lowercased
    obfuscated = "_AbC123"
    assert fwd_normalize_address(obfuscated) == obfuscated

import re
import pytest
from sanic.headers import fwd_normalize_address

def test_fwd_normalize_address_basic_cases():
    # IPv4 address should be lowercased (already lowercase)
    assert fwd_normalize_address("192.168.1.1") == "192.168.1.1"

    # IPv6 address should be bracketed and lowercased
    ipv6 = "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
    assert fwd_normalize_address(ipv6) == f"[{ipv6.lower()}]"

    # Obfuscated string starting with underscore should remain unchanged
    obfuscated = "_secret"
    assert fwd_normalize_address(obfuscated) == obfuscated

def test_fwd_normalize_address_unknown_raises():
    # The string "unknown" must raise ValueError
    with pytest.raises(ValueError):
        fwd_normalize_address("unknown")

def test_fwd_normalize_address_edge_cases():
    # Empty string should be returned unchanged (lowercased is same)
    assert fwd_normalize_address("") == ""

    # Mixed case IPv6 should be lowercased and bracketed
    mixed_case_ipv6 = "2001:DB8:85A3:0:0:8A2E:0370:7334"
    expected = f"[{mixed_case_ipv6.lower()}]"
    assert fwd_normalize_address(mixed_case_ipv6) == expected

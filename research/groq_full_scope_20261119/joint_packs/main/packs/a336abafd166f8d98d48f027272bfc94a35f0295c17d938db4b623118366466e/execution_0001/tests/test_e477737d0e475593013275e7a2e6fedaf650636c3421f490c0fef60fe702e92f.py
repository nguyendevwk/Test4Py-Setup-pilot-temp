import re
import pytest
from sanic.headers import fwd_normalize_address

def test_normalize_ipv4_and_ipv6_addresses():
    # IPv4 address should be lowercased (no change for digits/periods)
    assert fwd_normalize_address("192.168.1.1") == "192.168.1.1"

    # IPv6 address should be bracketed and lowercased
    ipv6 = "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
    expected = f"[{ipv6.lower()}]"
    assert fwd_normalize_address(ipv6) == expected

def test_obfuscated_and_unknown_values():
    # Leading underscore should preserve case and not be lowercased
    obfuscated = "_AbC123"
    assert fwd_normalize_address(obfuscated) == obfuscated

    # "unknown" should raise ValueError
    with pytest.raises(ValueError):
        fwd_normalize_address("unknown")

def test_edge_cases_and_invalid_inputs():
    # Empty string should be returned unchanged (lowercasing has no effect)
    assert fwd_normalize_address("") == ""

    # Address with mixed case letters should be lowercased
    mixed = "ExAmPlE.com"
    assert fwd_normalize_address(mixed) == mixed.lower()

    # Address that is not a valid IPv6 but contains colons should not be bracketed
    # e.g., a hostname with colon
    hostname = "example:80"
    assert fwd_normalize_address(hostname) == hostname.lower()

import pytest
from sanic.headers import fwd_normalize_address

def test_normal_ipv4_and_obfuscated():
    # Normal IPv4 address should be lowercased (no change for IPv4)
    assert fwd_normalize_address("192.168.1.1") == "192.168.1.1"
    # Obfuscated string starting with underscore should be returned unchanged
    assert fwd_normalize_address("_hidden") == "_hidden"

def test_ipv6_bracketing_and_lowercasing():
    # IPv6 address should be bracketed and lowercased
    ipv6 = "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
    expected = f"[{ipv6.lower()}]"
    assert fwd_normalize_address(ipv6) == expected
    # Mixed case IPv6 should also be lowercased inside brackets
    mixed = "2001:DB8:85A3:0:0:8A2E:0370:7334"
    assert fwd_normalize_address(mixed) == f"[{mixed.lower()}]"

def test_unknown_raises_value_error():
    # The string "unknown" must raise ValueError
    with pytest.raises(ValueError):
        fwd_normalize_address("unknown")

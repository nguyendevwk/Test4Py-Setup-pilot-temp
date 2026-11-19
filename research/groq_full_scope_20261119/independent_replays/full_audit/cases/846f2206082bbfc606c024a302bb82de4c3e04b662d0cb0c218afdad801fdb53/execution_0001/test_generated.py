import pytest
from sanic.headers import fwd_normalize_address

def test_normal_ipv4_and_obfuscated(tmp_path):
    # Normal IPv4 should be lowercased (no change) and returned unchanged
    assert fwd_normalize_address("192.168.1.1") == "192.168.1.1"

    # Obfuscated string starting with underscore should be returned unchanged
    assert fwd_normalize_address("_hidden") == "_hidden"

def test_ipv6_bracketing_and_lowercasing():
    # IPv6 address should be wrapped in brackets and lowercased
    ipv6 = "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
    expected = f"[{ipv6.lower()}]"
    assert fwd_normalize_address(ipv6) == expected

    # Mixed case IPv6 should also be lowercased and bracketed
    mixed = "2001:DB8:85A3:0:0:8A2E:0370:7334"
    expected_mixed = f"[{mixed.lower()}]"
    assert fwd_normalize_address(mixed) == expected_mixed

def test_unknown_raises_value_error():
    # The string "unknown" should raise a ValueError
    with pytest.raises(ValueError):
        fwd_normalize_address("unknown")

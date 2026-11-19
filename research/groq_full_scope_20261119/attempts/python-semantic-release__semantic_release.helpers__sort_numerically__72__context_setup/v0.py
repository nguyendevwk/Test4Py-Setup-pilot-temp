import pytest
from semantic_release.helpers import sort_numerically

def test_sort_numerically_basic_numbers():
    items = ["v2", "v10", "v1", "alpha", "beta"]
    result = sort_numerically(items)
    # Alphabetical prefixes first: 'alpha', 'beta', then numeric groups by prefix 'v'
    assert result == ["alpha", "beta", "v1", "v2", "v10"]

def test_sort_numerically_reverse_and_unmatched():
    items = ["v2", "v10", "v1", "gamma", "delta"]
    result = sort_numerically(items, reverse=True)
    # Unmatched items sorted alphabetically, then numeric group reversed
    assert result == ["delta", "gamma", "v10", "v2", "v1"]

def test_sort_numerically_hex_numbers():
    items = ["v0xA", "v0x5", "v0x10", "v3", "v2"]
    result = sort_numerically(items, allow_hex=True)
    # Hex numbers interpreted as hex, decimal numbers as decimal
    # Prefix 'v' group sorted by numeric value: 5, 10, 2, 3
    assert result == ["v0x5", "v0xA", "v0x10", "v2", "v3"]

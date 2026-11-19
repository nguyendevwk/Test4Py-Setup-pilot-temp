import pytest
from semantic_release.helpers import sort_numerically

def test_sort_numerically_basic():
    items = ["v2", "v10", "v1", "alpha", "beta"]
    result = sort_numerically(items)
    # Alphabetical prefixes first: alpha, beta, then v1, v2, v10
    assert result == ["alpha", "beta", "v1", "v2", "v10"]

def test_sort_numerically_hex_and_reverse():
    items = ["0x10", "0x2", "0xA", "foo", "bar"]
    # allow_hex=True, reverse=True should sort hex numbers descending
    result = sort_numerically(items, reverse=True, allow_hex=True)
    # bar and foo have no numbers, appear alphabetically before hex numbers
    assert result == ["bar", "foo", "0x10", "0xA", "0x2"]

def test_sort_numerically_no_numbers():
    items = ["alpha", "beta", "gamma"]
    result = sort_numerically(items)
    # All items have no numbers, should remain alphabetically sorted
    assert result == ["alpha", "beta", "gamma"]

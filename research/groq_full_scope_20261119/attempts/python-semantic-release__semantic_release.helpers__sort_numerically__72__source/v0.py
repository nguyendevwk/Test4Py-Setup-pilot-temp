import pytest
from semantic_release.helpers import sort_numerically

def test_sort_numerically_basic_numbers():
    items = ["v1.2", "v1.10", "v1.3", "alpha", "beta"]
    # Expected: alphabetic prefixes first, then numeric sorted ascending
    expected = ["alpha", "beta", "v1.2", "v1.3", "v1.10"]
    assert sort_numerically(items) == expected

def test_sort_numerically_hex_and_reverse():
    items = ["0x1A", "0x10", "0x2", "0x1", "foo"]
    # With allow_hex=True, numbers are interpreted as hex; reverse=True sorts descending
    expected = ["foo", "0x2", "0x1A", "0x10", "0x1"]
    assert sort_numerically(items, reverse=True, allow_hex=True) == expected

def test_sort_numerically_no_numbers():
    items = ["alpha", "beta", "gamma"]
    # No numeric parts; order should remain alphabetically sorted
    expected = ["alpha", "beta", "gamma"]
    assert sort_numerically(items) == expected

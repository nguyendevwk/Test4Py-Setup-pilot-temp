import pytest
from semantic_release.helpers import sort_numerically

def test_sort_numerically_basic_numbers():
    items = ["v1.2", "v1.10", "v1.3", "v1.1"]
    # Should sort numerically by the number after the prefix
    result = sort_numerically(items)
    assert result == ["v1.1", "v1.2", "v1.3", "v1.10"]

def test_sort_numerically_hex_and_reverse():
    items = ["vA", "v10", "v5", "vB"]
    # Allow hex interpretation and reverse numeric order
    result = sort_numerically(items, reverse=True, allow_hex=True)
    # Hex values: A=10, B=11, 10=16, 5=5
    # Reverse numeric order: 16, 11, 10, 5
    assert result == ["v10", "vB", "vA", "v5"]

def test_sort_numerically_unmatched_items():
    items = ["alpha", "beta1", "gamma", "delta2", "epsilon"]
    # Items without a numeric suffix should appear alphabetically among prefixes
    result = sort_numerically(items)
    # Expected order: alpha, beta1, delta2, epsilon, gamma
    assert result == ["alpha", "beta1", "delta2", "epsilon", "gamma"]

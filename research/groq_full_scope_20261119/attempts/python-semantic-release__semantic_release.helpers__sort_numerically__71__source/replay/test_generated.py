import pytest
from semantic_release.helpers import sort_numerically

def test_sort_numerically_basic_numbers():
    items = ["v1.0", "v2.0", "v10.0", "alpha", "beta"]
    result = sort_numerically(items)
    # "alpha" and "beta" are unmatched, sorted alphabetically before numeric prefixes
    assert result == ["alpha", "beta", "v1.0", "v2.0", "v10.0"]

def test_sort_numerically_hex_allowed():
    items = ["v1A", "v1B", "v1C", "v1a", "v1b", "v1c"]
    # Without hex, these are unmatched; with hex allowed, they are sorted numerically
    result_no_hex = sort_numerically(items, allow_hex=False)
    assert result_no_hex == sorted(items)  # all unmatched, alphabetically sorted

    result_hex = sort_numerically(items, allow_hex=True)
    # hex numbers 1A,1B,1C,1a,1b,1c are 26,27,28,26,27,28 respectively
    assert result_hex == ["v1A", "v1a", "v1B", "v1b", "v1C", "v1c"]

def test_sort_numerically_reverse_and_mixed_prefixes():
    items = ["release3", "release10", "release2", "dev1", "dev2", "dev10"]
    # Reverse numeric order within each prefix
    result = sort_numerically(items, reverse=True)
    # Prefixes sorted alphabetically: dev, release
    assert result == ["dev10", "dev2", "dev1", "release10", "release3", "release2"]

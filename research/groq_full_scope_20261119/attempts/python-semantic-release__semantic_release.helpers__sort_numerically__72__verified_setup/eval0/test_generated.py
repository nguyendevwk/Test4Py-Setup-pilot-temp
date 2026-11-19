import pytest
from semantic_release.helpers import sort_numerically

def test_sort_numerically_basic():
    """Verify that numeric suffixes are sorted correctly and prefixes are preserved."""
    items = ["v1.2", "v1.10", "v1.3", "alpha", "beta"]
    expected = ["alpha", "beta", "v1.2", "v1.3", "v1.10"]
    assert sort_numerically(items) == expected

def test_sort_numerically_hex_and_reverse():
    """Check that hexadecimal numbers are interpreted when allow_hex=True and reverse ordering works."""
    items = ["item0x10", "item0x2", "item0xA", "item0x1"]
    # With allow_hex=True, 0xA (10) > 0x10 (16) > 0x2 (2) > 0x1 (1)
    expected_desc = ["item0x10", "item0xA", "item0x2", "item0x1"]
    assert sort_numerically(items, reverse=True, allow_hex=True) == expected_desc
    # Without allow_hex, all are treated as non-numeric and sorted alphabetically
    expected_alpha = sorted(items)
    assert sort_numerically(items, allow_hex=False) == expected_alpha

def test_sort_numerically_invalid_input():
    """Ensure that passing a non-iterable raises a TypeError."""
    with pytest.raises(TypeError):
        sort_numerically(42)  # type: ignore[arg-type]

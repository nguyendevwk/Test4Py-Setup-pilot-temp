import pytest
from httpie.utils import is_version_greater

def test_normal_comparison():
    # Standard semantic version comparison
    assert is_version_greater("1.2.3", "1.2.2") is True
    assert is_version_greater("2.0.0", "1.9.9") is True
    assert is_version_greater("1.2.3", "1.2.3") is False
    assert is_version_greater("1.2.3", "1.2.4") is False

def test_boundary_and_non_numeric():
    # Versions with fewer components or non‑numeric suffixes
    assert is_version_greater("1.2", "1.2.0") is False  # (1,2) vs (1,2,0)
    assert is_version_greater("1.2.0", "1.2") is True   # (1,2,0) vs (1,2)
    assert is_version_greater("1.2a", "1.2.1") is False  # stops at non‑int
    assert is_version_greater("1.2.1", "1.2a") is True   # (1,2,1) > (1,2)

def test_empty_and_invalid_inputs():
    # Empty strings and completely invalid versions
    assert is_version_greater("", "0.0.1") is False
    assert is_version_greater("0.0.1", "") is True
    assert is_version_greater("", "") is False

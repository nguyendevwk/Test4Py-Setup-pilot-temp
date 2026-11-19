import pytest
from httpie.utils import is_version_greater

def test_basic_semver_comparison():
    # Normal case: higher patch version
    assert is_version_greater("1.2.3", "1.2.2") is True
    # Lower minor version
    assert is_version_greater("1.1.9", "1.2.0") is False
    # Major version difference
    assert is_version_greater("2.0.0", "1.9.9") is True

def test_boundary_equal_and_prefix():
    # Exactly equal versions
    assert is_version_greater("1.2.3", "1.2.3") is False
    # Prefix comparison: shorter tuple is considered smaller
    assert is_version_greater("1.2", "1.2.0") is False
    # Longer tuple with same prefix is greater
    assert is_version_greater("1.2.1", "1.2") is True

def test_non_numeric_parts_and_error_handling():
    # Non-numeric part stops parsing; comparison uses only parsed parts
    assert is_version_greater("1.2a.3", "1.2.2") is False
    # Leading non-numeric part results in empty tuple; always False
    assert is_version_greater("a.b.c", "0.0.1") is False
    # Mixed numeric and non-numeric: only numeric parts considered
    assert is_version_greater("3.0b", "2.9.9") is True

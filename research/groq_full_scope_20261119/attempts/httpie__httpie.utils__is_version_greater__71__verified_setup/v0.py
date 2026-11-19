import pytest
from httpie.utils import is_version_greater

def test_semver_comparison_basic():
    # Basic semantic version comparison
    assert is_version_greater("1.2.3", "1.2") is True
    assert is_version_greater("1.2.3", "1.2.3") is False
    assert is_version_greater("1.2.3", "1.2.10") is False

def test_non_numeric_part_handling():
    # Non-numeric parts stop parsing; comparison uses only numeric prefix
    assert is_version_greater("1.2a.3", "1.2") is False
    assert is_version_greater("1.2a.3", "1.1") is True
    assert is_version_greater("1.2.3", "1.2a.3") is True

def test_empty_and_short_versions():
    # Empty string and short versions are handled gracefully
    assert is_version_greater("", "0") is False
    assert is_version_greater("0", "") is True
    assert is_version_greater("0.0.1", "0.0") is True
    assert is_version_greater("0.0", "0.0.1") is False

import pytest
from string_utils.validation import is_isbn_10

def test_valid_isbn_with_hyphens():
    # ISBN 10 with hyphens should be accepted when normalize=True
    assert is_isbn_10("0-306-40615-2") is True
    # ISBN 10 without hyphens should also be accepted
    assert is_isbn_10("0306406152") is True

def test_invalid_isbn_and_normalization_flag():
    # Incorrect checksum should fail
    assert is_isbn_10("0-306-40615-3") is False
    # Hyphens present but normalization disabled should fail
    assert is_isbn_10("0-306-40615-2", normalize=False) is False
    # Non-digit characters should fail
    assert is_isbn_10("0-306-40615-X") is False

def test_boundary_cases_and_edge_inputs():
    # Minimum length ISBN 10 with all zeros
    assert is_isbn_10("0000000000") is True
    # ISBN 10 with 'X' as checksum
    assert is_isbn_10("030640615X") is True
    # Too short string should fail
    assert is_isbn_10("123456789") is False
    # Too long string should fail
    assert is_isbn_10("12345678901") is False

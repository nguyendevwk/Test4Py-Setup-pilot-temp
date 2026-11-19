import pytest
from httpie.utils import humanize_bytes

def test_humanize_bytes_basic_units():
    # Test that small values are represented in bytes and larger values in kB, MB, GB
    assert humanize_bytes(1) == "1 B"
    assert humanize_bytes(512) == "512.00 B"
    assert humanize_bytes(1024) == "1.00 kB"
    assert humanize_bytes(1024 * 123) == "123.00 kB"
    assert humanize_bytes(1024 * 12342) == "12.10 MB"
    assert humanize_bytes(1024 * 12342, precision=2) == "12.05 MB"
    assert humanize_bytes(1024 * 1234 * 1111) == "1.31 GB"

def test_humanize_bytes_precision_and_suffix():
    # Verify that the precision argument controls the number of decimal places
    assert humanize_bytes(1024 * 123, precision=1) == "123.0 kB"
    assert humanize_bytes(1024 * 123, precision=3) == "123.000 kB"
    # Check that the suffix changes correctly at the boundary of 1 TB
    assert humanize_bytes(1 << 40) == "1.00 TB"
    assert humanize_bytes((1 << 40) - 1) == "1023.99 GB"

def test_humanize_bytes_negative_and_zero():
    # The function does not explicitly handle negative values; it should still return a string
    assert humanize_bytes(-1024) == "-1.00 kB"
    # Zero should fall through to the last suffix 'B'
    assert humanize_bytes(0) == "0.00 B"

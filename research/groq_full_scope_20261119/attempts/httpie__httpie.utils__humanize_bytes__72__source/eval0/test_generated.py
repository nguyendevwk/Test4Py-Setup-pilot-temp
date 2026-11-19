import pytest
from httpie.utils import humanize_bytes

def test_humanize_bytes_basic_units():
    # 1 byte
    assert humanize_bytes(1) == "1 B"
    # 1 kB with default precision
    assert humanize_bytes(1024) == "1.00 kB"
    # 123 kB with one decimal
    assert humanize_bytes(1024 * 123, precision=1) == "123.0 kB"
    # 12.05 MB with two decimals
    assert humanize_bytes(1024 * 12342, precision=2) == "12.05 MB"

def test_humanize_bytes_boundary_values():
    # Just below 1 kB should still be in bytes
    assert humanize_bytes(1023) == "1023.00 B"
    # Exactly 1 MB
    assert humanize_bytes(1024 * 1024) == "1.00 MB"
    # Large value crossing into GB
    assert humanize_bytes(1024 * 1024 * 1024) == "1.00 GB"
    # Very large value crossing into TB
    assert humanize_bytes(1024 ** 4) == "1.00 TB"

def test_humanize_bytes_negative_and_precision():
    # Negative values are formatted with the same precision
    assert humanize_bytes(-1024, precision=1) == "-1.0 kB"
    # Zero should be handled as 0 B
    assert humanize_bytes(0) == "0.00 B"
    # Precision can be zero, yielding integer-like output
    assert humanize_bytes(1024 * 5, precision=0) == "5 kB"

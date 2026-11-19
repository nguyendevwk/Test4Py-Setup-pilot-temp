import pytest
from httpie.utils import humanize_bytes

def test_humanize_bytes_basic_units():
    # 1 byte should be special‑cased
    assert humanize_bytes(1) == "1 B"
    # 1024 bytes -> 1.00 kB with default precision
    assert humanize_bytes(1024) == "1.00 kB"
    # 1024 * 123 bytes -> 123.00 kB
    assert humanize_bytes(1024 * 123) == "123.00 kB"
    # 1024 * 12342 bytes -> 12.05 MB with precision 2
    assert humanize_bytes(1024 * 12342, precision=2) == "12.05 MB"

def test_humanize_bytes_precision_and_large_units():
    # 1024 * 1234 * 1111 bytes -> 1.31 GB with precision 2
    assert humanize_bytes(1024 * 1234 * 1111, precision=2) == "1.31 GB"
    # Same value with precision 1 should round to 1.3 GB
    assert humanize_bytes(1024 * 1234 * 1111, precision=1) == "1.3 GB"
    # 1 << 40 bytes (1 TB) should be formatted correctly
    assert humanize_bytes(1 << 40) == "1.00 TB"

def test_humanize_bytes_negative_and_zero():
    # Negative values are formatted with a negative sign and the appropriate unit
    assert humanize_bytes(-1024) == "-1.00 kB"
    # Zero bytes should fall back to the smallest unit
    assert humanize_bytes(0) == "0.00 B"

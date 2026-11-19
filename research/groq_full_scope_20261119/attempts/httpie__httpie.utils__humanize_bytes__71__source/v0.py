import pytest
from httpie.utils import humanize_bytes

def test_humanize_bytes_basic_and_precision():
    # Basic conversion with default precision
    assert humanize_bytes(1) == '1 B'
    assert humanize_bytes(1024) == '1.00 kB'
    # Precision adjustment
    assert humanize_bytes(1024 * 123, precision=1) == '123.0 kB'
    assert humanize_bytes(1024 * 12342, precision=2) == '12.05 MB'
    # Larger unit
    assert humanize_bytes(1024 * 1234 * 1111, precision=2) == '1.31 GB'

def test_humanize_bytes_boundary_values():
    # Exact power of two boundaries
    assert humanize_bytes(1 << 10) == '1.00 kB'
    assert humanize_bytes(1 << 20) == '1.00 MB'
    assert humanize_bytes(1 << 30) == '1.00 GB'
    # Just below a boundary should use the next lower unit
    assert humanize_bytes((1 << 20) - 1) == '1023.99 kB'
    # Just above a boundary should use the next higher unit
    assert humanize_bytes((1 << 20) + 1) == '1.00 MB'

def test_humanize_bytes_negative_and_zero():
    # Zero bytes should be represented as '0.00 B'
    assert humanize_bytes(0) == '0.00 B'
    # Negative values are handled by the same logic, yielding negative units
    assert humanize_bytes(-1024) == '-1024.00 B'
    # Negative values that cross a boundary still use the lowest unit
    assert humanize_bytes(- (1 << 20)) == '-1048576.00 B'

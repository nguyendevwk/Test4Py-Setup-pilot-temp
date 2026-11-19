import pytest
from httpie.utils import humanize_bytes

def test_humanize_bytes_basic_and_precision():
    # Basic conversion with default precision
    assert humanize_bytes(1) == '1 B'
    assert humanize_bytes(1024) == '1.00 kB'
    # Precision argument changes number of decimal places
    assert humanize_bytes(1024, precision=1) == '1.0 kB'
    assert humanize_bytes(1024 * 123, precision=1) == '123.0 kB'
    assert humanize_bytes(1024 * 12342, precision=2) == '12.05 MB'
    # Verify that rounding occurs correctly
    assert humanize_bytes(1024 * 1234, precision=2) == '1.21 MB'
    assert humanize_bytes(1024 * 1234 * 1111, precision=1) == '1.3 GB'

def test_humanize_bytes_boundary_values():
    # Zero bytes should be represented as 0.00 B with default precision
    assert humanize_bytes(0) == '0.00 B'
    # Very large number crossing multiple thresholds
    large = (1 << 50) + 123  # just over 1 PB
    assert humanize_bytes(large, precision=0) == '1 PB'
    # Ensure that the function chooses the largest factor <= n
    assert humanize_bytes(1024 * 1024 - 1) == '1023.99 kB'  # just below 1 MB

def test_humanize_bytes_invalid_input():
    # Passing a negative number should still produce a string but with negative sign
    assert humanize_bytes(-1024) == '-1.00 kB'
    # Passing a non-integer type should raise a TypeError due to division
    with pytest.raises(TypeError):
        humanize_bytes('1024')

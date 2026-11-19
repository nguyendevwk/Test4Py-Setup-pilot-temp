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
    # Larger values
    assert humanize_bytes(1024 * 1234 * 1111, precision=2) == '1.31 GB'

def test_humanize_bytes_boundary_values():
    # Zero bytes should be handled gracefully
    assert humanize_bytes(0) == '0.00 B'
    # Very large number crossing multiple thresholds
    large = (1 << 50) + 123  # just over 1 PB
    assert humanize_bytes(large, precision=0) == f'{large / (1 << 50):.0f} PB'
    # Ensure that the function chooses the largest applicable factor
    assert humanize_bytes(1024 * 1024 - 1) == '1023.99 kB'  # just below 1 MB

def test_humanize_bytes_invalid_input():
    # Negative numbers are not explicitly handled; function will still compute
    assert humanize_bytes(-1024) == '-1.00 kB'
    # Non-integer numeric types are accepted
    assert humanize_bytes(1024.5) == '1.00 kB'
    # Passing a non-numeric type should raise a TypeError
    with pytest.raises(TypeError):
        humanize_bytes("1024")

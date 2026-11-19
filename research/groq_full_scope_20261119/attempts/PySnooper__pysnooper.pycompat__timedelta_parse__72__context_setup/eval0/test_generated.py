import pytest
from pysnooper.pycompat import timedelta_parse
import datetime as datetime_module

def test_timedelta_parse_normal():
    # Normal case with all components
    td = timedelta_parse("2:30:15:500000")
    assert td == datetime_module.timedelta(hours=2, minutes=30, seconds=15, microseconds=500000)
    # Verify individual attributes
    assert td.total_seconds() == 2 * 3600 + 30 * 60 + 15
    assert td.microseconds == 500000

def test_timedelta_parse_boundary_values():
    # Boundary case: zero values
    td_zero = timedelta_parse("0:0:0:0")
    assert td_zero == datetime_module.timedelta(0)
    # Large values that still fit in int
    td_large = timedelta_parse("1000:59:59:999999")
    assert td_large == datetime_module.timedelta(hours=1000, minutes=59, seconds=59, microseconds=999999)
    # Check that the total seconds match expected calculation
    expected_seconds = 1000 * 3600 + 59 * 60 + 59
    assert td_large.total_seconds() == expected_seconds
    assert td_large.microseconds == 999999

def test_timedelta_parse_invalid_input():
    # Invalid format should raise ValueError
    with pytest.raises(ValueError):
        timedelta_parse("invalid:format")
    with pytest.raises(ValueError):
        timedelta_parse("1:2")  # missing components
    with pytest.raises(ValueError):
        timedelta_parse("1:2:3:4:5")  # too many components
    with pytest.raises(ValueError):
        timedelta_parse("1:2:3:abc")  # non-integer microseconds

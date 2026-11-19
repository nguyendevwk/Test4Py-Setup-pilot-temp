import pytest
import datetime as datetime_module
from pysnooper.pycompat import timedelta_parse

def test_timedelta_parse_normal():
    # Normal case with all components present
    td = timedelta_parse("02:30:15.123456")
    assert td == datetime_module.timedelta(hours=2, minutes=30, seconds=15, microseconds=123456)
    # Verify individual attributes
    assert td.total_seconds() == 2 * 3600 + 30 * 60 + 15
    assert td.microseconds == 123456

def test_timedelta_parse_boundary_large_values():
    # Boundary case with large numbers
    td = timedelta_parse("1000:59:59.999999")
    assert td == datetime_module.timedelta(hours=1000, minutes=59, seconds=59, microseconds=999999)
    # Check that the total seconds reflect the large hour value
    expected_seconds = 1000 * 3600 + 59 * 60 + 59
    assert td.total_seconds() == expected_seconds
    assert td.microseconds == 999999

def test_timedelta_parse_invalid_input():
    # Invalid string should raise ValueError due to int conversion failure
    with pytest.raises(ValueError):
        timedelta_parse("invalid:time:string")
    # Missing components should also raise ValueError
    with pytest.raises(ValueError):
        timedelta_parse("01:02")  # only two parts instead of four

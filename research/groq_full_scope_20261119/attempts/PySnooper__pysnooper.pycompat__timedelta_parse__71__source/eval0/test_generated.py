import pytest
import datetime as datetime_module
from pysnooper.pycompat import timedelta_parse

def test_timedelta_parse_normal():
    # Normal case with all components present
    td = timedelta_parse("2:30:15.123456")
    assert td == datetime_module.timedelta(hours=2, minutes=30, seconds=15, microseconds=123456)
    # Verify individual attributes
    assert td.total_seconds() == 2 * 3600 + 30 * 60 + 15
    assert td.microseconds == 123456

def test_timedelta_parse_boundary_values():
    # Test with maximum reasonable values for each component
    td = timedelta_parse("23:59:59.999999")
    assert td == datetime_module.timedelta(hours=23, minutes=59, seconds=59, microseconds=999999)
    # Ensure that the total seconds match the expected value
    expected_seconds = 23 * 3600 + 59 * 60 + 59
    assert td.total_seconds() == expected_seconds
    # Microseconds should be exactly 999999
    assert td.microseconds == 999999

def test_timedelta_parse_invalid_input():
    # Provide a string that cannot be parsed into four integer components
    with pytest.raises(ValueError):
        timedelta_parse("invalid:time:string")
    # Also test a string with too few components
    with pytest.raises(ValueError):
        timedelta_parse("1:2")
    # Test a string with non-integer values
    with pytest.raises(ValueError):
        timedelta_parse("1:2:three.4")

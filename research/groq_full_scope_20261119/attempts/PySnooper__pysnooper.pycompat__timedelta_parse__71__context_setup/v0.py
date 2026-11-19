import pytest
from pysnooper.pycompat import timedelta_parse
import datetime as datetime_module

def test_timedelta_parse_basic():
    """Verify that a standard time string is parsed correctly."""
    td = timedelta_parse("1:30:45.123456")
    assert td == datetime_module.timedelta(hours=1, minutes=30, seconds=45, microseconds=123456)
    assert td.total_seconds() == 1 * 3600 + 30 * 60 + 45 + 0.123456

def test_timedelta_parse_boundary_values():
    """Check parsing with large numbers and zero components."""
    td = timedelta_parse("100:0:0.0")
    assert td == datetime_module.timedelta(hours=100)
    td = timedelta_parse("0:0:0.999999")
    assert td == datetime_module.timedelta(microseconds=999999)

def test_timedelta_parse_invalid_input():
    """Ensure that malformed strings raise a ValueError."""
    with pytest.raises(ValueError):
        timedelta_parse("invalid")
    with pytest.raises(ValueError):
        timedelta_parse("1:2")  # missing components
    with pytest.raises(ValueError):
        timedelta_parse("1:2:3:4:5")  # too many components

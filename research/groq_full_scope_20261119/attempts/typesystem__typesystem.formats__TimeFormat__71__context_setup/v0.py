import datetime
import pytest
from typesystem.formats import TimeFormat

def test_valid_time_string_parses_correctly():
    fmt = TimeFormat()
    result = fmt.validate("12:34:56.789")
    assert isinstance(result, datetime.time)
    assert result.hour == 12
    assert result.minute == 34
    assert result.second == 56
    assert result.microsecond == 789000
    # serialization should round-trip
    assert fmt.serialize(result) == "12:34:56.789"

def test_boundary_time_with_max_microseconds():
    fmt = TimeFormat()
    result = fmt.validate("23:59:59.999999")
    assert result.hour == 23
    assert result.minute == 59
    assert result.second == 59
    assert result.microsecond == 999999
    # ensure isoformat includes full microseconds
    assert fmt.serialize(result) == "23:59:59.999999"

def test_invalid_time_raises_validation_error():
    fmt = TimeFormat()
    # invalid format (missing colon)
    with pytest.raises(Exception) as excinfo:
        fmt.validate("123456")
    assert "format" in str(excinfo.value)
    # invalid time value (hour out of range)
    with pytest.raises(Exception) as excinfo2:
        fmt.validate("24:00")
    assert "invalid" in str(excinfo2.value)

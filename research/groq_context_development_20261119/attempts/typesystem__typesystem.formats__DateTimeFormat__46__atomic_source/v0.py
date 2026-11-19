import datetime
import pytest
from typesystem.formats import DateTimeFormat

# Test 1: Valid datetime string with timezone offset and microseconds
def test_datetimeformat_valid_with_offset_and_microseconds():
    fmt = DateTimeFormat()
    input_str = "2023-07-15T12:34:56.789+02:30"
    result = fmt.validate(input_str)
    assert isinstance(result, datetime.datetime)
    assert result.year == 2023
    assert result.month == 7
    assert result.day == 15
    assert result.hour == 12
    assert result.minute == 34
    assert result.second == 56
    assert result.microsecond == 789000
    assert result.tzinfo == datetime.timezone(datetime.timedelta(hours=2, minutes=30))

# Test 2: Microsecond padding when fewer than 6 digits are provided
def test_datetimeformat_microsecond_padding():
    fmt = DateTimeFormat()
    input_str = "2023-01-01T00:00:00.1Z"
    result = fmt.validate(input_str)
    assert result.microsecond == 100000  # '1' padded to '100000'
    assert result.tzinfo == datetime.timezone.utc

# Test 3: Invalid format raises ValidationError
def test_datetimeformat_invalid_format_raises():
    fmt = DateTimeFormat()
    invalid_str = "not-a-datetime"
    with pytest.raises(Exception) as excinfo:
        fmt.validate(invalid_str)
    assert "Must be a valid datetime format." in str(excinfo.value)

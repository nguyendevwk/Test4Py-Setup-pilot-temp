import datetime
import pytest
from typesystem.formats import DateTimeFormat

# Test 1: Valid datetime string with timezone and microseconds
def test_datetimeformat_valid_with_timezone_and_microseconds():
    fmt = DateTimeFormat()
    input_str = "2023-07-15T12:34:56.789012+02:30"
    result = fmt.validate(input_str)
    assert isinstance(result, datetime.datetime)
    assert result.year == 2023
    assert result.month == 7
    assert result.day == 15
    assert result.hour == 12
    assert result.minute == 34
    assert result.second == 56
    assert result.microsecond == 789012
    assert result.tzinfo == datetime.timezone(datetime.timedelta(hours=2, minutes=30))

# Test 2: Valid datetime string with 'Z' timezone and missing microseconds
def test_datetimeformat_valid_with_z_and_no_microseconds():
    fmt = DateTimeFormat()
    input_str = "2023-07-15T12:34:56Z"
    result = fmt.validate(input_str)
    assert isinstance(result, datetime.datetime)
    assert result.year == 2023
    assert result.month == 7
    assert result.day == 15
    assert result.hour == 12
    assert result.minute == 34
    assert result.second == 56
    assert result.microsecond == 0
    assert result.tzinfo == datetime.timezone.utc

# Test 3: Invalid format and invalid date raise ValidationError
def test_datetimeformat_invalid_cases():
    fmt = DateTimeFormat()
    # Invalid format: missing time part
    with pytest.raises(fmt.ValidationError):
        fmt.validate("2023-07-15")
    # Invalid date: February 30th
    with pytest.raises(fmt.ValidationError):
        fmt.validate("2023-02-30T00:00:00Z")

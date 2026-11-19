import datetime
import pytest
from typesystem.formats import DateTimeFormat

# Test 1: Normal parsing of a datetime string without timezone
def test_datetime_parsing_without_timezone():
    fmt = DateTimeFormat()
    input_str = "2023-07-15T12:34:56"
    result = fmt.validate(input_str)
    assert isinstance(result, datetime.datetime)
    assert result.year == 2023
    assert result.month == 7
    assert result.day == 15
    assert result.hour == 12
    assert result.minute == 34
    assert result.second == 56
    assert result.microsecond == 0
    assert result.tzinfo is None

# Test 2: Parsing a datetime string with UTC timezone and microseconds
def test_datetime_parsing_with_utc_and_microseconds():
    fmt = DateTimeFormat()
    input_str = "2023-07-15T12:34:56.123Z"
    result = fmt.validate(input_str)
    assert isinstance(result, datetime.datetime)
    assert result.year == 2023
    assert result.month == 7
    assert result.day == 15
    assert result.hour == 12
    assert result.minute == 34
    assert result.second == 56
    assert result.microsecond == 123000  # padded to 6 digits
    assert result.tzinfo == datetime.timezone.utc

# Test 3: Invalid format should raise ValidationError
def test_datetime_invalid_format_raises_error():
    fmt = DateTimeFormat()
    invalid_input = "2023-07-15 12:34:56"  # space instead of 'T'
    with pytest.raises(Exception) as excinfo:
        fmt.validate(invalid_input)
    # The exception should be a ValidationError with message "Must be a valid datetime format."
    assert "Must be a valid datetime format." in str(excinfo.value)

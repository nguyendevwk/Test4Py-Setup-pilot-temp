import datetime
import pytest
from typesystem.formats import DateTimeFormat

# Test normal parsing of a full ISO 8601 datetime string with UTC timezone
def test_validate_full_iso_utc():
    fmt = DateTimeFormat()
    input_str = "2023-07-21T15:30:45.123456Z"
    result = fmt.validate(input_str)
    assert isinstance(result, datetime.datetime)
    assert result.year == 2023
    assert result.month == 7
    assert result.day == 21
    assert result.hour == 15
    assert result.minute == 30
    assert result.second == 45
    assert result.microsecond == 123456
    assert result.tzinfo == datetime.timezone.utc

# Test boundary case: microseconds with fewer than 6 digits should be padded
def test_validate_microsecond_padding():
    fmt = DateTimeFormat()
    input_str = "2023-07-21T15:30:45.1Z"
    result = fmt.validate(input_str)
    assert result.microsecond == 100000  # '1' padded to '100000'

# Test error handling: invalid date (e.g., February 30th) should raise ValidationError
def test_validate_invalid_date_raises():
    fmt = DateTimeFormat()
    input_str = "2023-02-30T00:00:00Z"
    with pytest.raises(Exception) as excinfo:
        fmt.validate(input_str)
    # The exception should be a ValidationError with the 'invalid' message
    assert hasattr(excinfo.value, "message")
    assert "Must be a real datetime." in str(excinfo.value)

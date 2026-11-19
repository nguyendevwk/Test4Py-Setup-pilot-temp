import datetime
import pytest
from typesystem.formats import DateTimeFormat

# Test 1: Valid ISO 8601 string with UTC timezone and microseconds
def test_datetimeformat_valid_utc_with_microseconds():
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
    # Serialization should preserve the Z suffix
    serialized = fmt.serialize(result)
    assert serialized == "2023-07-21T15:30:45.123456Z"

# Test 2: Valid ISO 8601 string with positive timezone offset and missing microseconds
def test_datetimeformat_valid_offset_no_microseconds():
    fmt = DateTimeFormat()
    input_str = "2023-12-01T08:00:00+02:30"
    result = fmt.validate(input_str)
    assert isinstance(result, datetime.datetime)
    assert result.year == 2023
    assert result.month == 12
    assert result.day == 1
    assert result.hour == 8
    assert result.minute == 0
    assert result.second == 0
    assert result.microsecond == 0
    assert result.tzinfo == datetime.timezone(datetime.timedelta(hours=2, minutes=30))
    # Serialization should convert to ISO format with offset
    serialized = fmt.serialize(result)
    assert serialized == "2023-12-01T08:00:00+02:30"

# Test 3: Invalid format and invalid date should raise ValidationError
def test_datetimeformat_invalid_cases():
    fmt = DateTimeFormat()
    # Invalid format: missing time part
    with pytest.raises(fmt.ValidationError):
        fmt.validate("2023-07-21")
    # Invalid date: February 30th
    with pytest.raises(fmt.ValidationError):
        fmt.validate("2023-02-30T12:00:00Z")

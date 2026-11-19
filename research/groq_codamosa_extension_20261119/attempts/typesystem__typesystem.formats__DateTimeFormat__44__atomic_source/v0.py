import datetime
import pytest
from typesystem.formats import DateTimeFormat

# Test 1: Normal valid datetime string with timezone offset
def test_datetimeformat_valid_with_offset():
    fmt = DateTimeFormat()
    input_str = "2023-07-15T12:34:56+02:00"
    result = fmt.validate(input_str)
    assert isinstance(result, datetime.datetime)
    assert result.year == 2023
    assert result.month == 7
    assert result.day == 15
    assert result.hour == 12
    assert result.minute == 34
    assert result.second == 56
    assert result.tzinfo == datetime.timezone(datetime.timedelta(hours=2))

# Test 2: Microsecond padding and UTC 'Z' handling
def test_datetimeformat_microseconds_and_z():
    fmt = DateTimeFormat()
    input_str = "2023-07-15T12:34:56.123Z"
    result = fmt.validate(input_str)
    assert result.microsecond == 123000  # padded to 6 digits
    assert result.tzinfo == datetime.timezone.utc
    # Serialize should convert back to ISO with 'Z'
    serialized = fmt.serialize(result)
    assert serialized == "2023-07-15T12:34:56.123000Z"

# Test 3: Invalid format and invalid date raise ValidationError
def test_datetimeformat_invalid_cases():
    fmt = DateTimeFormat()
    # Wrong format: missing time part
    with pytest.raises(fmt.ValidationError):
        fmt.validate("2023-07-15")
    # Invalid date: February 30th
    with pytest.raises(fmt.ValidationError):
        fmt.validate("2023-02-30T00:00:00Z")

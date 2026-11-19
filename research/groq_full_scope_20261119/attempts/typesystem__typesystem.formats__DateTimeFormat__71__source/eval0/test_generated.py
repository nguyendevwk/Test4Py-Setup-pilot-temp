import datetime
import pytest
from typesystem.formats import DateTimeFormat

# Test normal parsing of a full ISO 8601 datetime with timezone offset
def test_datetime_format_valid_with_offset():
    fmt = DateTimeFormat()
    input_str = "2023-07-15T12:34:56+02:30"
    result = fmt.validate(input_str)
    assert isinstance(result, datetime.datetime)
    assert result.year == 2023
    assert result.month == 7
    assert result.day == 15
    assert result.hour == 12
    assert result.minute == 34
    assert result.second == 56
    assert result.microsecond == 0
    assert result.tzinfo == datetime.timezone(datetime.timedelta(hours=2, minutes=30))

# Test parsing of a datetime with microseconds and UTC designator
def test_datetime_format_microseconds_and_utc():
    fmt = DateTimeFormat()
    input_str = "2021-01-01T00:00:00.123+00:00"
    result = fmt.validate(input_str)
    assert result == datetime.datetime(2021, 1, 1, 0, 0, 0, 123000, tzinfo=datetime.timezone.utc)

    # Serialize back to string and check that UTC is represented with 'Z'
    serialized = fmt.serialize(result)
    assert serialized == "2021-01-01T00:00:00.123Z"

# Test that an invalid format raises a ValidationError with the correct message
def test_datetime_format_invalid_format():
    fmt = DateTimeFormat()
    invalid_str = "not-a-datetime"
    with pytest.raises(Exception) as excinfo:
        fmt.validate(invalid_str)
    # The exception should be a ValidationError with the 'format' error message
    assert hasattr(excinfo.value, "message")
    assert "Must be a valid datetime format." in str(excinfo.value)

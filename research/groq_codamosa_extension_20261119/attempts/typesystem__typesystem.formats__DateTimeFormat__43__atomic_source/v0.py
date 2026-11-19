import datetime
import pytest
from typesystem.formats import DateTimeFormat

# Test 1: Normal valid datetime string with UTC offset
def test_datetimeformat_valid_utc():
    fmt = DateTimeFormat()
    dt_str = "2023-07-15T12:34:56.789Z"
    result = fmt.validate(dt_str)
    assert isinstance(result, datetime.datetime)
    assert result == datetime.datetime(2023, 7, 15, 12, 34, 56, 789000, tzinfo=datetime.timezone.utc)
    serialized = fmt.serialize(result)
    assert serialized == "2023-07-15T12:34:56.789Z"

# Test 2: Boundary case with timezone offset and microseconds
def test_datetimeformat_timezone_offset_and_microseconds():
    fmt = DateTimeFormat()
    dt_str = "2023-01-01T00:00:00.1+02:30"
    result = fmt.validate(dt_str)
    assert result == datetime.datetime(2023, 1, 1, 0, 0, 0, 100000, tzinfo=datetime.timezone(datetime.timedelta(hours=2, minutes=30)))
    serialized = fmt.serialize(result)
    assert serialized == "2023-01-01T00:00:00.100000+02:30"

# Test 3: Invalid format and invalid date should raise ValidationError
def test_datetimeformat_invalid():
    fmt = DateTimeFormat()
    # Invalid format: missing seconds
    with pytest.raises(fmt.ValidationError):
        fmt.validate("2023-07-15T12:34Z")
    # Invalid date: February 30th
    with pytest.raises(fmt.ValidationError):
        fmt.validate("2023-02-30T12:00:00Z")

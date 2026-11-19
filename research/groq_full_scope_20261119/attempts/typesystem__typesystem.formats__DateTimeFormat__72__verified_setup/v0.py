import datetime
import pytest
from typesystem.formats import DateTimeFormat

# Test 1: Valid ISO 8601 datetime string with UTC timezone
def test_validate_and_serialize_basic_utc():
    fmt = DateTimeFormat()
    input_str = "2023-07-21T15:30:45Z"
    dt = fmt.validate(input_str)
    assert isinstance(dt, datetime.datetime)
    assert dt == datetime.datetime(2023, 7, 21, 15, 30, 45, tzinfo=datetime.timezone.utc)
    serialized = fmt.serialize(dt)
    assert serialized == "2023-07-21T15:30:45Z"

# Test 2: Valid datetime string with microseconds and positive offset
def test_validate_microseconds_and_offset():
    fmt = DateTimeFormat()
    input_str = "2023-07-21T15:30:45.123+02:00"
    dt = fmt.validate(input_str)
    assert dt == datetime.datetime(2023, 7, 21, 15, 30, 45, 123000,
                                    tzinfo=datetime.timezone(datetime.timedelta(hours=2)))
    # serialization should preserve the offset in ISO format
    serialized = fmt.serialize(dt)
    assert serialized == "2023-07-21T15:30:45.123+02:00"

# Test 3: Invalid format should raise ValidationError
def test_validate_invalid_format_raises():
    fmt = DateTimeFormat()
    with pytest.raises(fmt.ValidationError) as excinfo:
        fmt.validate("not-a-datetime")
    assert "format" in str(excinfo.value)

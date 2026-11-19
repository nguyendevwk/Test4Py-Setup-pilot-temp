import datetime
import pytest
from typesystem.formats import DateTimeFormat

def test_valid_datetime_with_timezone_and_microseconds():
    fmt = DateTimeFormat()
    # ISO string with UTC timezone and 3‑digit microseconds
    iso_str = "2023-07-15T12:34:56.789Z"
    result = fmt.validate(iso_str)
    assert isinstance(result, datetime.datetime)
    assert result == datetime.datetime(2023, 7, 15, 12, 34, 56, 789000, tzinfo=datetime.timezone.utc)
    # Serialization should preserve the Z suffix
    serialized = fmt.serialize(result)
    assert serialized == iso_str

def test_boundary_microseconds_and_negative_offset():
    fmt = DateTimeFormat()
    # 6‑digit microseconds and negative offset
    iso_str = "2024-01-01T00:00:00.123456-02:30"
    result = fmt.validate(iso_str)
    assert result == datetime.datetime(2024, 1, 1, 0, 0, 0, 123456,
                                        tzinfo=datetime.timezone(datetime.timedelta(hours=-2, minutes=-30)))
    # Serialize back to ISO format with correct offset
    serialized = fmt.serialize(result)
    assert serialized == "2024-01-01T00:00:00.123456-02:30"

def test_invalid_datetime_raises_validation_error():
    fmt = DateTimeFormat()
    # Invalid month (13) should trigger ValueError in datetime constructor
    iso_str = "2023-13-01T00:00:00Z"
    with pytest.raises(Exception) as excinfo:
        fmt.validate(iso_str)
    # The exception should be a ValidationError with code "invalid"
    assert hasattr(excinfo.value, "code") and excinfo.value.code == "invalid"
    # The message should match the defined error text
    assert "Must be a real datetime." in str(excinfo.value)

import datetime
import pytest
from typesystem.formats import DateTimeFormat

def test_valid_datetime_with_timezone_and_microseconds():
    fmt = DateTimeFormat()
    # ISO string with timezone offset and 3‑digit microseconds
    iso_str = "2024-11-19T12:34:56.789+02:00"
    result = fmt.validate(iso_str)
    assert isinstance(result, datetime.datetime)
    assert result.year == 2024
    assert result.month == 11
    assert result.day == 19
    assert result.hour == 12
    assert result.minute == 34
    assert result.second == 56
    assert result.microsecond == 789000  # padded to 6 digits
    assert result.tzinfo == datetime.timezone(datetime.timedelta(hours=2))

def test_serialize_utc_z_suffix():
    fmt = DateTimeFormat()
    dt = datetime.datetime(2024, 11, 19, 12, 34, 56, tzinfo=datetime.timezone.utc)
    serialized = fmt.serialize(dt)
    # UTC should be represented with a trailing 'Z'
    assert serialized == "2024-11-19T12:34:56Z"

def test_invalid_datetime_raises_validation_error():
    fmt = DateTimeFormat()
    # Invalid month (13) and missing timezone
    bad_str = "2024-13-01T00:00:00"
    with pytest.raises(Exception) as excinfo:
        fmt.validate(bad_str)
    # The exception should be a ValidationError with code "invalid"
    assert hasattr(excinfo.value, "code")
    assert excinfo.value.code == "invalid"
    assert "Must be a real datetime." in str(excinfo.value)

import datetime
import pytest
from typesystem.formats import DateTimeFormat

def test_valid_datetime_parsing_and_serialization():
    fmt = DateTimeFormat()
    # ISO string with timezone offset
    iso_str = "2023-07-21T15:30:45.123456+02:00"
    dt = fmt.validate(iso_str)
    assert isinstance(dt, datetime.datetime)
    assert dt.year == 2023
    assert dt.month == 7
    assert dt.day == 21
    assert dt.hour == 15
    assert dt.minute == 30
    assert dt.second == 45
    assert dt.microsecond == 123456
    assert dt.tzinfo == datetime.timezone(datetime.timedelta(hours=2))
    # Serialization should preserve the same format (offset)
    assert fmt.serialize(dt) == iso_str

def test_microsecond_padding_and_zulu_timezone():
    fmt = DateTimeFormat()
    # Microsecond part shorter than 6 digits, should be padded
    iso_str = "2023-07-21T15:30:45.1Z"
    dt = fmt.validate(iso_str)
    assert dt.microsecond == 100000  # padded to 6 digits
    assert dt.tzinfo == datetime.timezone.utc
    # Serialization should convert UTC to 'Z'
    assert fmt.serialize(dt) == "2023-07-21T15:30:45.100000Z"

def test_invalid_datetime_raises_validation_error():
    fmt = DateTimeFormat()
    # Invalid month (13) should raise ValueError inside datetime constructor
    with pytest.raises(fmt.validation_error("").__class__) as excinfo:
        fmt.validate("2023-13-01T00:00:00Z")
    assert "invalid" in excinfo.value.code
    # Invalid format (missing time part) should raise format error
    with pytest.raises(fmt.validation_error("").__class__) as excinfo:
        fmt.validate("2023-07-01")
    assert "format" in excinfo.value.code

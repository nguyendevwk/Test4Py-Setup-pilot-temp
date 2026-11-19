import datetime
import pytest
from typesystem.formats import DateTimeFormat

# Test 1: Normal parsing and serialization of a UTC datetime with 'Z' suffix
def test_datetimeformat_parse_and_serialize_utc():
    fmt = DateTimeFormat()
    # ISO 8601 string with UTC designator
    input_str = "2023-07-15T12:34:56Z"
    parsed = fmt.validate(input_str)
    assert isinstance(parsed, datetime.datetime)
    assert parsed.year == 2023
    assert parsed.month == 7
    assert parsed.day == 15
    assert parsed.hour == 12
    assert parsed.minute == 34
    assert parsed.second == 56
    assert parsed.tzinfo == datetime.timezone.utc

    serialized = fmt.serialize(parsed)
    assert serialized == "2023-07-15T12:34:56Z"

# Test 2: Parsing a datetime with fractional seconds and a positive timezone offset
def test_datetimeformat_parse_fractional_and_offset():
    fmt = DateTimeFormat()
    # 3 fractional digits, offset +02:30
    input_str = "2021-12-31T23:59:59.123+02:30"
    parsed = fmt.validate(input_str)
    assert parsed.microsecond == 123000  # padded to 6 digits
    assert parsed.tzinfo == datetime.timezone(datetime.timedelta(hours=2, minutes=30))

    # Serialize back and compare
    serialized = fmt.serialize(parsed)
    # isoformat will use +02:30
    assert serialized == "2021-12-31T23:59:59.123+02:30"

# Test 3: Invalid format should raise ValidationError
def test_datetimeformat_invalid_format_raises():
    fmt = DateTimeFormat()
    # Missing 'T' separator
    bad_input = "2023-07-15 12:34:56"
    with pytest.raises(fmt.ValidationError) as excinfo:
        fmt.validate(bad_input)
    assert "format" in str(excinfo.value)

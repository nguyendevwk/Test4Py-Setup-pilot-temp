import datetime
import pytest
from typesystem.formats import DateTimeFormat

# Test 1: Valid ISO‑8601 datetime string with UTC timezone ("Z")
def test_validate_valid_datetime_z():
    fmt = DateTimeFormat()
    input_str = "2023-08-15T12:34:56Z"
    result = fmt.validate(input_str)
    assert isinstance(result, datetime.datetime)
    assert result.year == 2023
    assert result.month == 8
    assert result.day == 15
    assert result.hour == 12
    assert result.minute == 34
    assert result.second == 56
    assert result.microsecond == 0
    assert result.tzinfo == datetime.timezone.utc
    # Serialize back to string
    serialized = fmt.serialize(result)
    assert serialized == "2023-08-15T12:34:56Z"

# Test 2: Invalid format string should raise ValidationError
def test_validate_invalid_format():
    fmt = DateTimeFormat()
    bad_str = "not-a-datetime"
    with pytest.raises(fmt.ValidationError) as excinfo:
        fmt.validate(bad_str)
    assert "format" in str(excinfo.value)

# Test 3: Valid format but impossible date (e.g., Feb 30) should raise ValidationError
def test_validate_invalid_date():
    fmt = DateTimeFormat()
    impossible_str = "2023-02-30T00:00:00"
    with pytest.raises(fmt.ValidationError) as excinfo:
        fmt.validate(impossible_str)
    assert "invalid" in str(excinfo.value)

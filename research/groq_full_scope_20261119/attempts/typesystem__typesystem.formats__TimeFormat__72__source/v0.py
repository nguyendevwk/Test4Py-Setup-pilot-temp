import datetime
import pytest
from typesystem.formats import TimeFormat

# Test 1: Valid time string with microseconds
def test_timeformat_valid_with_microseconds():
    fmt = TimeFormat()
    # 12:34:56.789123 is a valid time
    result = fmt.validate("12:34:56.789123")
    assert isinstance(result, datetime.time)
    assert result.hour == 12
    assert result.minute == 34
    assert result.second == 56
    assert result.microsecond == 789123
    # Serialization should return the same ISO format
    assert fmt.serialize(result) == "12:34:56.789123"

# Test 2: Boundary case – maximum valid time
def test_timeformat_boundary_max_time():
    fmt = TimeFormat()
    # 23:59:59.999999 is the maximum valid time
    result = fmt.validate("23:59:59.999999")
    assert result == datetime.time(23, 59, 59, 999999)
    # Serialize and compare
    assert fmt.serialize(result) == "23:59:59.999999"

# Test 3: Invalid format and invalid time value
def test_timeformat_invalid_cases():
    fmt = TimeFormat()
    # Invalid format: missing seconds
    with pytest.raises(fmt.ValidationError) as excinfo_format:
        fmt.validate("12:34")
    assert "format" in str(excinfo_format.value)

    # Invalid time: hour out of range
    with pytest.raises(fmt.ValidationError) as excinfo_invalid:
        fmt.validate("24:00:00")
    assert "invalid" in str(excinfo_invalid.value)

    # None serialization returns None
    assert fmt.serialize(None) is None

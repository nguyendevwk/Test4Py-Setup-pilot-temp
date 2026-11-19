import datetime
import pytest
from typesystem.formats import TimeFormat

# Test 1: Valid time string with all components
def test_timeformat_valid_full():
    fmt = TimeFormat()
    # 12:34:56.789123 is a valid time
    result = fmt.validate("12:34:56.789123")
    assert isinstance(result, datetime.time)
    assert result.hour == 12
    assert result.minute == 34
    assert result.second == 56
    assert result.microsecond == 789123
    # Serialization should return ISO format
    assert fmt.serialize(result) == "12:34:56.789123"

# Test 2: Boundary case – maximum valid time with microseconds
def test_timeformat_boundary_max():
    fmt = TimeFormat()
    # 23:59:59.999999 is the latest possible time
    result = fmt.validate("23:59:59.999999")
    assert result == datetime.time(23, 59, 59, 999999)
    # Serialize back to string
    assert fmt.serialize(result) == "23:59:59.999999"

# Test 3: Invalid format and invalid time values
def test_timeformat_invalid():
    fmt = TimeFormat()
    # Wrong format: missing colon
    with pytest.raises(fmt.validation_error("").__class__):
        fmt.validate("123456")
    # Invalid hour value (24 is out of range)
    with pytest.raises(fmt.validation_error("").__class__):
        fmt.validate("24:00")
    # Invalid minute value (60 is out of range)
    with pytest.raises(fmt.validation_error("").__class__):
        fmt.validate("23:60")

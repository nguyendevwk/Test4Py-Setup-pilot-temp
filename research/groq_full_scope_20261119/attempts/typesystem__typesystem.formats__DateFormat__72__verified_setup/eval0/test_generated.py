import datetime
import pytest
from typesystem.formats import DateFormat

# Test 1: Valid date string is parsed correctly
def test_dateformat_valid():
    fmt = DateFormat()
    # ISO format date string
    date_str = "2023-12-31"
    result = fmt.validate(date_str)
    assert isinstance(result, datetime.date)
    assert result == datetime.date(2023, 12, 31)

# Test 2: Invalid format raises ValidationError with correct message
def test_dateformat_invalid_format():
    fmt = DateFormat()
    bad_format = "31-12-2023"  # not ISO
    with pytest.raises(Exception) as excinfo:
        fmt.validate(bad_format)
    # The exception should be a ValidationError with the "format" message
    assert hasattr(excinfo.value, "message")
    assert "Must be a valid date format." in str(excinfo.value)

# Test 3: Real but impossible date raises ValidationError with correct message
def test_dateformat_invalid_real_date():
    fmt = DateFormat()
    impossible_date = "2023-02-30"  # February 30 does not exist
    with pytest.raises(Exception) as excinfo:
        fmt.validate(impossible_date)
    # The exception should be a ValidationError with the "invalid" message
    assert hasattr(excinfo.value, "message")
    assert "Must be a real date." in str(excinfo.value)

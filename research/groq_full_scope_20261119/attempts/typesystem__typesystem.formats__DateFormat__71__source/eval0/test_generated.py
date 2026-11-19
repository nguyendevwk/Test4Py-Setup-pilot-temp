import datetime
import pytest
from typesystem.formats import DateFormat

# Test 1: Valid date string should be parsed correctly
def test_dateformat_valid():
    fmt = DateFormat()
    result = fmt.validate("2023-12-31")
    assert isinstance(result, datetime.date)
    assert result == datetime.date(2023, 12, 31)

# Test 2: Invalid format should raise a ValidationError with the correct message
def test_dateformat_invalid_format():
    fmt = DateFormat()
    with pytest.raises(Exception) as excinfo:
        fmt.validate("31-12-2023")
    # The exception should be a ValidationError from typesystem.base
    assert hasattr(excinfo.value, "message")
    assert "Must be a valid date format." in str(excinfo.value)

# Test 3: Real but impossible date should raise a ValidationError with the correct message
def test_dateformat_invalid_date():
    fmt = DateFormat()
    with pytest.raises(Exception) as excinfo:
        fmt.validate("2023-02-30")
    assert hasattr(excinfo.value, "message")
    assert "Must be a real date." in str(excinfo.value)

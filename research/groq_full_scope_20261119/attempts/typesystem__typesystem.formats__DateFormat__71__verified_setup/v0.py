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

    # Serialization round‑trip
    serialized = fmt.serialize(result)
    assert serialized == date_str

# Test 2: Invalid format raises the correct ValidationError
def test_dateformat_invalid_format():
    fmt = DateFormat()
    # Missing month part
    bad_format = "2023-13"
    with pytest.raises(Exception) as excinfo:
        fmt.validate(bad_format)
    # The exception should be a ValidationError with the "format" message
    assert hasattr(excinfo.value, "message")
    assert "Must be a valid date format." in str(excinfo.value)

# Test 3: Real date validation (e.g., February 30) raises ValidationError
def test_dateformat_invalid_real_date():
    fmt = DateFormat()
    # February 30 is not a real date
    bad_date = "2023-02-30"
    with pytest.raises(Exception) as excinfo:
        fmt.validate(bad_date)
    # The exception should be a ValidationError with the "invalid" message
    assert hasattr(excinfo.value, "message")
    assert "Must be a real date." in str(excinfo.value)

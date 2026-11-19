import datetime
import pytest
from typesystem.formats import DateFormat

def test_valid_date_parsing_and_serialization():
    fmt = DateFormat()
    # Normal valid date string
    date_str = "2023-07-15"
    parsed = fmt.validate(date_str)
    assert isinstance(parsed, datetime.date)
    assert parsed == datetime.date(2023, 7, 15)
    # Serialization should return ISO format string
    assert fmt.serialize(parsed) == "2023-07-15"

def test_invalid_format_raises_validation_error():
    fmt = DateFormat()
    # Boundary case: wrong format (missing day)
    with pytest.raises(Exception) as excinfo:
        fmt.validate("2023-07")
    # Ensure the raised exception is a ValidationError with correct code
    assert excinfo.type.__name__ == "ValidationError"
    assert excinfo.value.code == "format"
    assert "Must be a valid date format." in str(excinfo.value)

def test_nonexistent_date_raises_validation_error():
    fmt = DateFormat()
    # Boundary case: February 30th does not exist
    with pytest.raises(Exception) as excinfo:
        fmt.validate("2023-02-30")
    # Ensure the raised exception is a ValidationError with correct code
    assert excinfo.type.__name__ == "ValidationError"
    assert excinfo.value.code == "invalid"
    assert "Must be a real date." in str(excinfo.value)

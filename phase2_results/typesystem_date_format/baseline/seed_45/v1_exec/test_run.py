import datetime
import pytest
from typesystem.formats import DateFormat

def test_dateformat_validate_correct_and_errors():
    fmt = DateFormat()
    # Valid date string should return a datetime.date instance
    assert fmt.validate("2023-08-15") == datetime.date(2023, 8, 15)

    # Invalid format should raise an exception with the format error message
    with pytest.raises(Exception) as excinfo:
        fmt.validate("15-08-2023")
    assert "Must be a valid date format." in str(excinfo.value)

    # Invalid date (e.g., Feb 30) should raise an exception with the invalid error message
    with pytest.raises(Exception) as excinfo:
        fmt.validate("2023-02-30")
    assert "Must be a real date." in str(excinfo.value)

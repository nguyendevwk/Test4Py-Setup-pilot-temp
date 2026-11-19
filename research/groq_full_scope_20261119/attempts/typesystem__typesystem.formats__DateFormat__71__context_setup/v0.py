import datetime
import pytest
from typesystem.formats import DateFormat

def test_validate_successful_date_parsing():
    fmt = DateFormat()
    # A valid date string that matches the regex
    date_str = "2023-07-15"
    result = fmt.validate(date_str)
    assert isinstance(result, datetime.date)
    assert result == datetime.date(2023, 7, 15)

def test_validate_invalid_format_raises_error():
    fmt = DateFormat()
    # String that does not match the expected YYYY-MM-DD pattern
    bad_format = "15/07/2023"
    with pytest.raises(Exception) as excinfo:
        fmt.validate(bad_format)
    # The raised exception should be a ValidationError with the correct code
    assert excinfo.value.code == "format"
    assert "Must be a valid date format." in str(excinfo.value)

def test_validate_nonexistent_date_raises_error():
    fmt = DateFormat()
    # February 30th does not exist; regex matches but date construction fails
    bad_date = "2023-02-30"
    with pytest.raises(Exception) as excinfo:
        fmt.validate(bad_date)
    # The raised exception should be a ValidationError with the correct code
    assert excinfo.value.code == "invalid"
    assert "Must be a real date." in str(excinfo.value)

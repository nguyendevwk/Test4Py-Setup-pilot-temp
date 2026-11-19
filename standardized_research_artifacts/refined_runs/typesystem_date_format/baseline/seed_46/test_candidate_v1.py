import datetime
import pytest
from typesystem.formats import DateFormat

def test_dateformat_validate_parses_and_errors():
    df = DateFormat()

    # Valid date string
    valid_str = "2023-12-31"
    result = df.validate(valid_str)
    assert isinstance(result, datetime.date)
    assert result == datetime.date(2023, 12, 31)

    # Invalid format
    with pytest.raises(Exception) as excinfo:
        df.validate("31-12-2023")
    assert "Must be a valid date format." in str(excinfo.value)

    # Invalid date
    with pytest.raises(Exception) as excinfo:
        df.validate("2023-02-30")
    assert "Must be a real date." in str(excinfo.value)

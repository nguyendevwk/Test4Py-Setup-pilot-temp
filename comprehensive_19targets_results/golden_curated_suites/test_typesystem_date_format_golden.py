import datetime
import pytest
from typesystem.formats import DateFormat

def test_date_format_behavior():
    df = DateFormat()

    # Valid date string
    date_str = "2023-12-31"
    result = df.validate(date_str)
    assert isinstance(result, datetime.date)
    assert result == datetime.date(2023, 12, 31)

    # Invalid format
    with pytest.raises(Exception) as excinfo:
        df.validate("2023/12/31")
    assert "Must be a valid date format." in str(excinfo.value)

    # Invalid date
    with pytest.raises(Exception) as excinfo:
        df.validate("2023-02-30")
    assert "Must be a real date." in str(excinfo.value)

    # is_native_type checks
    assert df.is_native_type(datetime.date(2023, 1, 1))
    assert not df.is_native_type("2023-01-01")

    # serialize behavior
    assert df.serialize(datetime.date(2023, 1, 1)) == "2023-01-01"
    assert df.serialize(None) is None

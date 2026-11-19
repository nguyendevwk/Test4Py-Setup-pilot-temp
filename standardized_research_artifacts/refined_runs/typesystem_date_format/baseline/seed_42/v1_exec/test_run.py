import datetime
import pytest
from typesystem.formats import DateFormat


def test_date_format_behavior():
    df = DateFormat()

    # Valid date string
    valid_str = "2023-12-31"
    expected_date = datetime.date(2023, 12, 31)
    assert df.validate(valid_str) == expected_date

    # Invalid format
    with pytest.raises(Exception) as excinfo:
        df.validate("31-12-2023")
    assert "Must be a valid date format." in str(excinfo.value)

    # Invalid date value
    with pytest.raises(Exception) as excinfo:
        df.validate("2023-02-30")
    assert "Must be a real date." in str(excinfo.value)

    # Serialization of None
    assert df.serialize(None) is None

    # Serialization of a valid date object
    date_obj = datetime.date(2021, 1, 1)
    assert df.serialize(date_obj) == "2021-01-01"

    # is_native_type checks
    assert df.is_native_type(date_obj) is True
    assert df.is_native_type("2021-01-01") is False

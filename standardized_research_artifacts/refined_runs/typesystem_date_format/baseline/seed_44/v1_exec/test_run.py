import datetime
import pytest
from typesystem.formats import DateFormat


def test_dateformat_validate_and_serialize():
    df = DateFormat()

    # Valid date string
    date_obj = df.validate("2023-07-15")
    assert isinstance(date_obj, datetime.date)
    assert date_obj == datetime.date(2023, 7, 15)

    # Invalid format
    with pytest.raises(Exception) as excinfo:
        df.validate("2023/07/15")
    assert "format" in str(excinfo.value)

    # Invalid real date
    with pytest.raises(Exception) as excinfo:
        df.validate("2023-02-30")
    assert "invalid" in str(excinfo.value)

    # Serialization of None
    assert df.serialize(None) is None

    # Serialization of a date object
    iso_str = df.serialize(datetime.date(2021, 12, 31))
    assert iso_str == "2021-12-31"

    # is_native_type checks
    assert df.is_native_type(datetime.date(2020, 1, 1))
    assert not df.is_native_type("2020-01-01")

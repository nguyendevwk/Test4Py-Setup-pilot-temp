import datetime
import pytest
from typesystem.formats import DateFormat


def test_dateformat_validate_and_serialize():
    fmt = DateFormat()
    date_str = "2023-07-15"
    date_obj = fmt.validate(date_str)
    assert isinstance(date_obj, datetime.date)
    assert date_obj.year == 2023 and date_obj.month == 7 and date_obj.day == 15
    iso = fmt.serialize(date_obj)
    assert iso == "2023-07-15"
    assert fmt.serialize(None) is None

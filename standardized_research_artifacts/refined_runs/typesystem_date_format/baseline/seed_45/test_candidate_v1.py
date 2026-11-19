import datetime
import pytest
from typesystem.formats import DateFormat

def test_dateformat_validate_parses_valid_date():
    fmt = DateFormat()
    result = fmt.validate("2023-07-15")
    assert isinstance(result, datetime.date)
    assert result == datetime.date(2023, 7, 15)

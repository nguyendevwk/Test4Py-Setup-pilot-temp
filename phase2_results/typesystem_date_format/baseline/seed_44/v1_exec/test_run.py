import pytest
import datetime
from typesystem.formats import DateFormat

def test_dateformat_validate_and_serialize():
    fmt = DateFormat()
    # is_native_type
    assert fmt.is_native_type(datetime.date(2020, 1, 1))
    assert not fmt.is_native_type("2020-01-01")
    # validate correct format
    d = fmt.validate("2020-01-01")
    assert isinstance(d, datetime.date) and d == datetime.date(2020, 1, 1)
    # validate wrong format
    with pytest.raises(Exception) as excinfo:
        fmt.validate("01-01-2020")
    assert "format" in str(excinfo.value)
    # validate invalid date
    with pytest.raises(Exception) as excinfo:
        fmt.validate("2021-02-30")
    assert "invalid" in str(excinfo.value)
    # serialize
    assert fmt.serialize(d) == "2020-01-01"
    assert fmt.serialize(None) is None
    # serialize wrong type
    with pytest.raises(AssertionError):
        fmt.serialize("2020-01-01")

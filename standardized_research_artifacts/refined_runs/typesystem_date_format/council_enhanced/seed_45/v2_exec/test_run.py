import datetime
import pytest
from typesystem.formats import DateFormat
from typesystem.base import ValidationError

def test_dateformat_behavior():
    fmt = DateFormat()

    # Valid date string
    dt = fmt.validate("2026-11-17")
    assert isinstance(dt, datetime.date)
    assert dt.year == 2026 and dt.month == 11 and dt.day == 17

    # Invalid format string
    with pytest.raises(ValidationError) as excinfo:
        fmt.validate("2026/11/17")
    assert excinfo.value.error_code == "format"

    # Invalid real date
    with pytest.raises(ValidationError) as excinfo:
        fmt.validate("2026-02-30")
    assert excinfo.value.error_code == "invalid"

    # Serialization of None
    assert fmt.serialize(None) is None

    # Serialization of a date object
    iso = fmt.serialize(dt)
    assert iso == "2026-11-17"

    # is_native_type checks
    assert fmt.is_native_type(dt) is True
    assert fmt.is_native_type(datetime.datetime.now()) is False
    assert fmt.is_native_type("2026-11-17") is False

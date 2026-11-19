import datetime
import pytest
from typesystem.formats import DateFormat
from typesystem.base import ValidationError

def test_date_format_validate_and_serialize():
    fmt = DateFormat()

    # native type detection
    assert fmt.is_native_type(datetime.date(2020, 1, 1)) is True
    assert fmt.is_native_type("2020-01-01") is False

    # valid date string
    dt = fmt.validate("2026-11-17")
    assert isinstance(dt, datetime.date)
    assert dt.year == 2026 and dt.month == 11 and dt.day == 17

    # invalid format
    with pytest.raises(ValidationError) as excinfo:
        fmt.validate("2026/11/17")
    assert excinfo.value.code == "format"

    # invalid date
    with pytest.raises(ValidationError) as excinfo:
        fmt.validate("2026-02-30")
    assert excinfo.value.code == "invalid"

    # serialization
    assert fmt.serialize(None) is None
    assert fmt.serialize(datetime.date(2026, 11, 17)) == "2026-11-17"

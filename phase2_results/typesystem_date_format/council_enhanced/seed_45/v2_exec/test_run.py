import datetime
import pytest
from typesystem.formats import DateFormat
from typesystem.base import ValidationError

def test_dateformat_validate_and_serialize():
    fmt = DateFormat()

    # Valid date string
    dt = fmt.validate("2026-11-17")
    assert isinstance(dt, datetime.date)
    assert dt.year == 2026 and dt.month == 11 and dt.day == 17

    # Invalid format (missing day)
    with pytest.raises(ValidationError) as excinfo:
        fmt.validate("2026-11")
    assert "format" in str(excinfo.value)

    # Invalid date (month out of range)
    with pytest.raises(ValidationError) as excinfo:
        fmt.validate("2026-13-01")
    assert "invalid" in str(excinfo.value)

    # Serialization of a date
    iso = fmt.serialize(dt)
    assert iso == "2026-11-17"

    # Serialization of None
    assert fmt.serialize(None) is None

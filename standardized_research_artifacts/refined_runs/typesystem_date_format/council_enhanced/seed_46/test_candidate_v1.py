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

    # Invalid format
    with pytest.raises(ValidationError) as excinfo:
        fmt.validate("2026/11/17")
    assert excinfo.value.code == "format"
    assert "Must be a valid date format." in excinfo.value.text

    # Invalid date (non‑existent day)
    with pytest.raises(ValidationError) as excinfo:
        fmt.validate("2026-02-30")
    assert excinfo.value.code == "invalid"
    assert "Must be a real date." in excinfo.value.text

    # Serialization
    assert fmt.serialize(dt) == "2026-11-17"
    assert fmt.serialize(None) is None

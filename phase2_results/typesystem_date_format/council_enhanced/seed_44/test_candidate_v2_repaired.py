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

    # Invalid format (does not match regex)
    with pytest.raises(ValidationError) as excinfo:
        fmt.validate("2026/11/17")
    assert excinfo.value.message == "Must be a valid date format."

    # Invalid date (real date check)
    with pytest.raises(ValidationError) as excinfo:
        fmt.validate("2026-13-01")  # month 13 is invalid
    assert excinfo.value.message == "Must be a real date."

    # is_native_type checks
    assert fmt.is_native_type(dt) is True
    assert fmt.is_native_type("2026-11-17") is False

    # Serialization
    assert fmt.serialize(dt) == "2026-11-17"
    assert fmt.serialize(None) is None

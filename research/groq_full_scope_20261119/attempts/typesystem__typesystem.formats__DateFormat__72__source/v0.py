import datetime
import pytest
from typesystem.formats import DateFormat
from typesystem.base import ValidationError

def test_dateformat_valid_normal():
    fmt = DateFormat()
    # A typical valid date string
    result = fmt.validate("2023-07-15")
    assert isinstance(result, datetime.date)
    assert result == datetime.date(2023, 7, 15)
    # Serialization should produce the same ISO string
    assert fmt.serialize(result) == "2023-07-15"

def test_dateformat_valid_boundary_leap_year():
    fmt = DateFormat()
    # February 29 on a leap year is a boundary case
    result = fmt.validate("2020-02-29")
    assert result == datetime.date(2020, 2, 29)
    # Ensure serialization matches ISO format
    assert fmt.serialize(result) == "2020-02-29"

def test_dateformat_invalid_inputs():
    fmt = DateFormat()
    # Wrong format should raise a format error
    with pytest.raises(ValidationError) as excinfo_format:
        fmt.validate("15-07-2023")
    assert "format" in str(excinfo_format.value)

    # Valid format but impossible date should raise an invalid error
    with pytest.raises(ValidationError) as excinfo_invalid:
        fmt.validate("2023-02-30")
    assert "invalid" in str(excinfo_invalid.value)

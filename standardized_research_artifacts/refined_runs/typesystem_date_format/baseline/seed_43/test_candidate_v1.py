import datetime
import pytest
from typesystem.formats import DateFormat

def test_date_format_validate_and_serialize():
    fmt = DateFormat()

    # Valid date string
    assert fmt.validate("2023-12-31") == datetime.date(2023, 12, 31)

    # Invalid format
    with pytest.raises(Exception) as excinfo:
        fmt.validate("2023/12/31")
    assert "format" in str(excinfo.value)

    # Invalid date
    with pytest.raises(Exception) as excinfo:
        fmt.validate("2023-02-30")
    assert "invalid" in str(excinfo.value)

    # Serialize None
    assert fmt.serialize(None) is None

    # Serialize a date object
    d = datetime.date(2021, 1, 1)
    assert fmt.serialize(d) == "2021-01-01"

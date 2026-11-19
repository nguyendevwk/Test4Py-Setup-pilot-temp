import datetime
import pytest
from typesystem.formats import DateFormat


def test_dateformat_validate_errors_and_success():
    df = DateFormat()

    # Valid date string
    assert df.validate("2023-02-28") == datetime.date(2023, 2, 28)

    # Invalid format
    with pytest.raises(Exception) as excinfo:
        df.validate("2023/02/28")
    assert "Must be a valid date format." in str(excinfo.value)

    # Invalid real date
    with pytest.raises(Exception) as excinfo:
        df.validate("2023-02-30")
    assert "Must be a real date." in str(excinfo.value)

    # Passing a datetime.date instance (not a string)
    with pytest.raises(Exception) as excinfo:
        df.validate(datetime.date(2023, 2, 28))
    assert "Must be a valid date format." in str(excinfo.value)

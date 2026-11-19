import datetime
import pytest
from typesystem.formats import TimeFormat

# Instantiate the format class
time_format = TimeFormat()


def test_valid_time_parsing_and_serialization():
    """Valid time string should be parsed to a datetime.time and serialized back."""
    time_str = "12:34:56.789"
    parsed = time_format.validate(time_str)
    assert isinstance(parsed, datetime.time)
    assert parsed.hour == 12
    assert parsed.minute == 34
    assert parsed.second == 56
    assert parsed.microsecond == 789000  # padded to 6 digits

    serialized = time_format.serialize(parsed)
    assert serialized == "12:34:56.789"


def test_invalid_format_raises_validation_error():
    """Strings that do not match the time regex should raise a format error."""
    with pytest.raises(Exception) as excinfo:
        time_format.validate("not-a-time")
    # The exception should be a ValidationError with the correct message
    assert hasattr(excinfo.value, "message")
    assert "Must be a valid time format." in excinfo.value.message


def test_invalid_time_value_raises_validation_error():
    """Valid format but impossible time (e.g., 25:00:00) should raise an invalid error."""
    with pytest.raises(Exception) as excinfo:
        time_format.validate("25:00:00")
    assert hasattr(excinfo.value, "message")
    assert "Must be a real time." in excinfo.value.message

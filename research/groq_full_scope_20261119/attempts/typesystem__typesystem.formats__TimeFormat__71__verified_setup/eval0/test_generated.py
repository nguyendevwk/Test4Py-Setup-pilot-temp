import datetime
import pytest
from typesystem.formats import TimeFormat

# Instantiate the format once for reuse
time_format = TimeFormat()


def test_valid_time_parsing_and_serialization():
    """A correctly formatted time string should be parsed into a datetime.time
    object and then serialized back to the same string."""
    input_str = "12:34:56.789"
    # Validate parses the string
    parsed = time_format.validate(input_str)
    assert isinstance(parsed, datetime.time)
    assert parsed.hour == 12
    assert parsed.minute == 34
    assert parsed.second == 56
    assert parsed.microsecond == 789000  # padded to 6 digits

    # Serialize returns the ISO format string
    serialized = time_format.serialize(parsed)
    assert serialized == "12:34:56.789000"


def test_invalid_format_raises_validation_error():
    """Strings that do not match the expected time format should raise a
    ValidationError with the 'format' message."""
    invalid_str = "not-a-time"
    with pytest.raises(Exception) as excinfo:
        time_format.validate(invalid_str)
    # The exception should be a ValidationError with the correct message
    assert hasattr(excinfo.value, "message")
    assert "Must be a valid time format." in str(excinfo.value)


def test_invalid_time_value_raises_validation_error():
    """A string that matches the regex but represents an impossible time
    (e.g., 25:61:61) should raise a ValidationError with the 'invalid'
    message."""
    impossible_str = "25:61:61"
    with pytest.raises(Exception) as excinfo:
        time_format.validate(impossible_str)
    assert hasattr(excinfo.value, "message")
    assert "Must be a real time." in str(excinfo.value)

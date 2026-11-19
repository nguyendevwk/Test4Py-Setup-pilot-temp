import datetime
import pytest
from typesystem.formats import TimeFormat

# Instantiate the format class
time_format = TimeFormat()


def test_validate_and_serialize_valid_time():
    """Test that a correctly formatted time string is parsed and serialized."""
    # A valid time string with microseconds
    time_str = "12:34:56.789"
    # Validate should return a datetime.time object
    result = time_format.validate(time_str)
    assert isinstance(result, datetime.time)
    assert result.hour == 12
    assert result.minute == 34
    assert result.second == 56
    # Microseconds should be padded to 6 digits
    assert result.microsecond == 789000

    # Serializing the resulting time should give the original string
    serialized = time_format.serialize(result)
    assert serialized == "12:34:56.789000"


def test_validate_invalid_format_raises():
    """Test that an incorrectly formatted string raises a format error."""
    # Missing seconds part
    bad_time_str = "12:34"
    with pytest.raises(Exception) as excinfo:
        time_format.validate(bad_time_str)
    # The exception should be a ValidationError with the correct message
    assert "Must be a valid time format." in str(excinfo.value)


def test_validate_invalid_time_value_raises():
    """Test that a string with an impossible time value raises an invalid error."""
    # Hour out of range
    bad_time_str = "25:00:00"
    with pytest.raises(Exception) as excinfo:
        time_format.validate(bad_time_str)
    # The exception should be a ValidationError with the correct message
    assert "Must be a real time." in str(excinfo.value)

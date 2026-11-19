import pytest
from pathlib import Path
from isort.exceptions import UnsupportedEncoding, ISortError


def test_unsupported_encoding_message_and_attribute(tmp_path):
    """Verify that the exception message contains the filename and the attribute is set."""
    file_path = tmp_path / "test.py"
    exc = UnsupportedEncoding(file_path)
    # The message should include the string representation of the Path
    assert str(file_path) in str(exc)
    # The filename attribute should be the same Path object
    assert exc.filename == file_path
    # The exception should be an instance of ISortError
    assert isinstance(exc, ISortError)


def test_unsupported_encoding_with_empty_string():
    """An empty string should still produce a valid message and attribute."""
    exc = UnsupportedEncoding("")
    assert str(exc) == "Unknown or unsupported encoding in "
    assert exc.filename == ""


def test_unsupported_encoding_with_non_string_input():
    """Passing a non-string (e.g., int) should be accepted and converted to a string."""
    exc = UnsupportedEncoding(42)
    assert str(exc) == "Unknown or unsupported encoding in 42"
    assert exc.filename == 42

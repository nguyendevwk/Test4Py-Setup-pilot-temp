import pytest
from pathlib import Path
from isort.exceptions import UnsupportedEncoding, ISortError


def test_unsupported_encoding_message_and_attribute(tmp_path: Path):
    """Normal case: a Path instance is passed and the exception stores it."""
    file_path = tmp_path / "test.py"
    exc = UnsupportedEncoding(file_path)
    # The message should include the string representation of the Path
    assert str(file_path) in str(exc)
    # The filename attribute should be the same Path object
    assert exc.filename is file_path
    # The exception should be an instance of ISortError
    assert isinstance(exc, ISortError)


def test_unsupported_encoding_with_empty_string():
    """Boundary case: an empty string is passed as the filename."""
    exc = UnsupportedEncoding("")
    # The message should still be constructed correctly
    assert str(exc) == "Unknown or unsupported encoding in "
    # The filename attribute should be the empty string
    assert exc.filename == ""


def test_unsupported_encoding_with_non_string_input():
    """Error behavior: passing a non-string, non-Path value should still work
    because the constructor accepts any object that can be converted to str."""
    non_str = 42
    exc = UnsupportedEncoding(non_str)
    # The message should contain the string representation of the integer
    assert str(exc) == "Unknown or unsupported encoding in 42"
    # The filename attribute should store the original value
    assert exc.filename == non_str

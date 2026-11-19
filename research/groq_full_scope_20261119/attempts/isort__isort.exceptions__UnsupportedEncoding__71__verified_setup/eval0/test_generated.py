import pytest
from pathlib import Path
from isort.exceptions import UnsupportedEncoding, ISortError


def test_unsupported_encoding_initialization_with_path(tmp_path):
    """Verify that the exception stores a Path object and formats the message correctly."""
    file_path = tmp_path / "example.py"
    exc = UnsupportedEncoding(file_path)
    # The filename attribute should be the same Path instance
    assert exc.filename is file_path
    # The message should include the string representation of the Path
    assert str(file_path) in str(exc)
    # The exception should be a subclass of ISortError
    assert isinstance(exc, ISortError)


def test_unsupported_encoding_with_empty_string():
    """Boundary case: an empty string should be accepted and reflected in the message."""
    exc = UnsupportedEncoding("")
    # The filename attribute should be the empty string
    assert exc.filename == ""
    # The message should contain the empty string (i.e., end with a space)
    assert str(exc).endswith(" in ")
    # Ensure the exception is still an instance of Exception
    assert isinstance(exc, Exception)


def test_unsupported_encoding_with_invalid_type():
    """Error behavior: passing a non-string/non-Path type should raise a TypeError."""
    with pytest.raises(TypeError):
        UnsupportedEncoding(123)  # type: ignore[arg-type]

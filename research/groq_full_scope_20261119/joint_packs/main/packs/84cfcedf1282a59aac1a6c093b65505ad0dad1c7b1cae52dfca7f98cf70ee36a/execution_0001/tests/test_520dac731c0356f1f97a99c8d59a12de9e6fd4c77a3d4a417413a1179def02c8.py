import pytest
from pathlib import Path
from isort.exceptions import UnsupportedEncoding


def test_unsupported_encoding_message_and_filename(tmp_path):
    """Verify that the exception message contains the filename and the filename attribute is set."""
    file_path = tmp_path / "test.py"
    exc = UnsupportedEncoding(file_path)
    # The message should include the string representation of the Path
    assert str(file_path) in str(exc)
    # The filename attribute should be the same Path object
    assert exc.filename == file_path


def test_unsupported_encoding_with_string_filename():
    """Ensure that a plain string filename is accepted and stored correctly."""
    filename = "example.py"
    exc = UnsupportedEncoding(filename)
    # The message should contain the string filename
    assert filename in str(exc)
    # The filename attribute should be the string
    assert exc.filename == filename


def test_unsupported_encoding_is_subclass_of_exception():
    """Confirm that UnsupportedEncoding behaves like a standard exception."""
    exc = UnsupportedEncoding("dummy.py")
    # It should be an instance of Exception and its own class
    assert isinstance(exc, Exception)
    assert isinstance(exc, UnsupportedEncoding)
    # The exception should be catchable by a generic Exception handler
    try:
        raise exc
    except Exception as e:
        assert e is exc

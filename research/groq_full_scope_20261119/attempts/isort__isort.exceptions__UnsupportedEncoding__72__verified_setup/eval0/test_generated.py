import pytest
from pathlib import Path
from isort.exceptions import UnsupportedEncoding


def test_unsupported_encoding_message_and_attribute(tmp_path):
    """The exception should store the filename and format the message correctly."""
    file_path = tmp_path / "test.py"
    exc = UnsupportedEncoding(file_path)
    # The message should include the string representation of the Path
    assert str(file_path) in str(exc)
    # The filename attribute should be the same object passed in
    assert exc.filename is file_path


def test_unsupported_encoding_with_string_filename():
    """Passing a plain string should work and produce the same message."""
    filename = "example.py"
    exc = UnsupportedEncoding(filename)
    assert str(exc) == f"Unknown or unsupported encoding in {filename}"
    assert exc.filename == filename


def test_unsupported_encoding_inherits_from_exception():
    """UnsupportedEncoding should be a subclass of Exception (via ISortError)."""
    exc = UnsupportedEncoding("dummy.py")
    assert isinstance(exc, Exception)
    # Ensure it is not caught by a generic Exception but can be caught by its own type
    try:
        raise exc
    except UnsupportedEncoding as e:
        assert e is exc
    except Exception:
        pytest.fail("Raised exception was not caught by UnsupportedEncoding")

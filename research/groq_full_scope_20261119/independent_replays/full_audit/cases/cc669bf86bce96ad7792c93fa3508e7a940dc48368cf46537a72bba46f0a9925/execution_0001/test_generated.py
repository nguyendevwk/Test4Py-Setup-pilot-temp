import pytest
from isort.exceptions import FileSkipped, ISortError


def test_fileskipped_attributes():
    """FileSkipped should store the message and file_path attributes."""
    msg = "Skipping due to unsupported format"
    path = "/tmp/example.py"
    exc = FileSkipped(msg, path)
    assert isinstance(exc, Exception)
    assert exc.message == msg
    assert exc.file_path == path
    # The base Exception message should be the same as the provided message
    assert str(exc) == msg


def test_fileskipped_inheritance():
    """FileSkipped must be a subclass of ISortError and Exception."""
    exc = FileSkipped("msg", "file.py")
    assert isinstance(exc, ISortError)
    assert isinstance(exc, Exception)
    # Ensure that the exception can be caught by an ISortError handler
    try:
        raise exc
    except ISortError as e:
        assert e is exc
    else:
        pytest.fail("FileSkipped was not caught by ISortError handler")


def test_fileskipped_empty_strings():
    """FileSkipped should handle empty strings without raising."""
    exc = FileSkipped("", "")
    assert exc.message == ""
    assert exc.file_path == ""
    # The string representation should also be empty
    assert str(exc) == ""

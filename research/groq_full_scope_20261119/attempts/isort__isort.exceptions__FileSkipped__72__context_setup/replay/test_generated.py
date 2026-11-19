import pytest
from isort.exceptions import FileSkipped, ISortError


def test_file_skipped_initialization():
    """FileSkipped should store message and file_path correctly."""
    msg = "Skipping due to unsupported format"
    path = "/tmp/example.py"
    exc = FileSkipped(msg, path)
    assert isinstance(exc, FileSkipped)
    assert exc.message == msg
    assert exc.file_path == path
    # The base Exception message should be the same as the provided message
    assert str(exc) == msg


def test_file_skipped_inheritance_and_cause():
    """FileSkipped must inherit from ISortError and Exception."""
    exc = FileSkipped("test", "file.py")
    # ISortError is the direct base class
    assert isinstance(exc, ISortError)
    # Exception is also a base class
    assert isinstance(exc, Exception)
    # No cause should be set by default
    assert exc.__cause__ is None
    assert exc.__context__ is None


def test_file_skipped_raising_and_catching():
    """Raising a FileSkipped should propagate correctly and preserve attributes."""
    msg = "File not found"
    path = "nonexistent.py"
    with pytest.raises(FileSkipped) as excinfo:
        raise FileSkipped(msg, path)
    raised = excinfo.value
    assert raised.message == msg
    assert raised.file_path == path
    # The exception should be caught as a generic Exception as well
    try:
        raise raised
    except Exception as e:
        assert isinstance(e, Exception)
        assert isinstance(e, FileSkipped)

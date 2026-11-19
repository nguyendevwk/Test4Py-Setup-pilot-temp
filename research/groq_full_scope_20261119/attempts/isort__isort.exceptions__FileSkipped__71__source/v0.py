import pytest
from isort.exceptions import FileSkipped


def test_file_skipped_initialization():
    """FileSkipped should store the message and file_path correctly."""
    msg = "Skipping due to unsupported format"
    path = "/tmp/example.py"
    exc = FileSkipped(msg, path)
    assert isinstance(exc, FileSkipped)
    assert exc.message == msg
    assert exc.file_path == path
    # The base Exception stores the message in args[0]
    assert exc.args[0] == msg


def test_file_skipped_inherits_from_exception():
    """FileSkipped must be a subclass of Exception and ISortError."""
    msg = "Test message"
    path = "file.py"
    exc = FileSkipped(msg, path)
    assert isinstance(exc, Exception)
    # ISortError is imported in the module; ensure subclass relationship
    from isort.exceptions import ISortError
    assert isinstance(exc, ISortError)


def test_file_skipped_raised_and_caught():
    """Raising FileSkipped should propagate the correct attributes."""
    msg = "Cannot process file"
    path = "nonexistent.py"
    with pytest.raises(FileSkipped) as excinfo:
        raise FileSkipped(msg, path)
    raised = excinfo.value
    assert raised.message == msg
    assert raised.file_path == path
    # Ensure the exception message is the same as the args[0]
    assert str(raised) == msg

import pytest
from isort.exceptions import FileSkipped


def test_file_skipped_initialization():
    """FileSkipped should store the message and file_path correctly."""
    msg = "Skipping due to unsupported format"
    path = "/tmp/example.py"
    exc = FileSkipped(msg, path)
    assert isinstance(exc, Exception)
    assert exc.message == msg
    assert exc.file_path == path
    # The base Exception message should be the same as the provided message
    assert str(exc) == msg


def test_file_skipped_raises_and_catches():
    """Raising FileSkipped should propagate the correct attributes."""
    msg = "File is not a Python file"
    path = "/tmp/not_python.txt"
    with pytest.raises(FileSkipped) as excinfo:
        raise FileSkipped(msg, path)
    exc = excinfo.value
    assert exc.message == msg
    assert exc.file_path == path
    # Ensure the exception is caught as the specific subclass
    assert isinstance(exc, FileSkipped)


def test_file_skipped_repr_and_hash():
    """FileSkipped should have a useful representation and be hashable."""
    msg = "Empty file"
    path = "/tmp/empty.py"
    exc = FileSkipped(msg, path)
    # Representation should include class name and message
    rep = repr(exc)
    assert "FileSkipped" in rep
    assert msg in rep
    # Hashing should be based on the underlying Exception hash
    assert hash(exc) == hash(str(exc))

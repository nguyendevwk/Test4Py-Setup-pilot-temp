import pytest
from isort.exceptions import FileSkipped, ISortError


def test_file_skipped_initialization():
    """FileSkipped should store the message and file_path attributes."""
    msg = "Skipping due to pattern"
    path = "/tmp/example.py"
    exc = FileSkipped(msg, path)
    assert isinstance(exc, FileSkipped)
    assert exc.message == msg
    assert exc.file_path == path
    # The base Exception message should be the same as the provided message
    assert str(exc) == msg


def test_file_skipped_inherits_isort_error():
    """FileSkipped must be a subclass of ISortError."""
    exc = FileSkipped("msg", "/path/file.py")
    assert isinstance(exc, ISortError)
    # Ensure that the exception can be caught by an ISortError handler
    try:
        raise exc
    except ISortError as e:
        assert e is exc
    else:
        pytest.fail("FileSkipped was not caught by ISortError handler")


def test_file_skipped_raises_and_catches(tmp_path):
    """Raising FileSkipped should propagate correctly and be caught."""
    file_path = tmp_path / "test.py"
    file_path.write_text("print('hello')")
    exc = FileSkipped("test skip", str(file_path))
    with pytest.raises(FileSkipped) as excinfo:
        raise exc
    assert excinfo.value.file_path == str(file_path)
    assert excinfo.value.message == "test skip"

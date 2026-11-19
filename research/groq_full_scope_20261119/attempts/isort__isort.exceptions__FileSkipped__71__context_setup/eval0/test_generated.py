import pytest
from isort.exceptions import FileSkipped, ISortError


def test_file_skipped_initialization_and_attributes():
    """FileSkipped should store message and file_path correctly."""
    msg = "Skipping due to pattern"
    path = "/tmp/example.py"
    exc = FileSkipped(msg, path)

    # The exception message should be the provided message
    assert str(exc) == msg
    # Custom attributes should be set
    assert exc.message == msg
    assert exc.file_path == path


def test_file_skipped_inherits_from_isort_error():
    """FileSkipped must be a subclass of ISortError."""
    exc = FileSkipped("msg", "file.py")
    # isinstance checks the inheritance chain
    assert isinstance(exc, ISortError)
    # The base Exception should also be present
    assert isinstance(exc, Exception)


def test_file_skipped_repr_and_str_consistency():
    """The string representation should match the message attribute."""
    exc = FileSkipped("Test message", "test.py")
    # str() uses the Exception's __str__, which should reflect the message
    assert str(exc) == exc.message
    # repr should include the class name and message for debugging
    assert repr(exc).startswith("<isort.exceptions.FileSkipped")
    assert "Test message" in repr(exc)

import pytest
from isort.exceptions import FileSkipComment


def test_file_skip_comment_message_and_attribute():
    """The exception should contain the file path in its message and expose it as an attribute."""
    fp = "example.py"
    exc = FileSkipComment(fp)
    # The message should mention the file path
    assert fp in str(exc)
    # The file_path attribute should be set correctly
    assert getattr(exc, "file_path") == fp


def test_file_skip_comment_inherits_from_FileSkipped():
    """FileSkipComment must be a subclass of FileSkipped."""
    fp = "test.py"
    exc = FileSkipComment(fp)
    # Import the base class directly to check inheritance
    from isort.exceptions import FileSkipped
    assert isinstance(exc, FileSkipped)


def test_file_skip_comment_accepts_additional_kwargs():
    """Any additional keyword arguments should be accepted and stored on the exception."""
    fp = "sample.py"
    extra = {"detail": "ignored"}
    exc = FileSkipComment(fp, **extra)
    # The exception should still have the file_path attribute
    assert exc.file_path == fp
    # The extra keyword arguments should be stored in the exception's __dict__
    assert exc.__dict__.get("detail") == "ignored"

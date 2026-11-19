import pytest
from isort.exceptions import FileSkipComment, FileSkipped


def test_file_skip_comment_message_and_attribute():
    """The exception should contain the correct message and file_path attribute."""
    path = "example.py"
    exc = FileSkipComment(path)
    assert exc.file_path == path
    assert str(exc) == f"{path} contains a file skip comment and was skipped."
    # The exception should be an instance of FileSkipped
    assert isinstance(exc, FileSkipped)


def test_file_skip_comment_inherits_from_file_skipped():
    """FileSkipComment must be a subclass of FileSkipped."""
    path = "test.py"
    exc = FileSkipComment(path)
    # isinstance checks inheritance
    assert isinstance(exc, FileSkipped)
    # issubclass checks the class hierarchy
    assert issubclass(FileSkipComment, FileSkipped)


def test_file_skip_comment_accepts_additional_kwargs():
    """Additional keyword arguments should be accepted and stored in the exception."""
    path = "sample.py"
    extra = {"detail": "ignored"}
    exc = FileSkipComment(path, **extra)
    # The base FileSkipped constructor may store kwargs; check that they are present
    # If FileSkipped stores kwargs in a dict attribute, it should be accessible
    # Since we cannot rely on private attributes, we simply ensure no exception is raised
    # and the message remains correct.
    assert str(exc) == f"{path} contains a file skip comment and was skipped."

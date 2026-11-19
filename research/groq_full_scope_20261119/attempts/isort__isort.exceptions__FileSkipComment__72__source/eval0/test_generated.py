import pytest
from isort.exceptions import FileSkipComment

def test_file_skip_comment_message():
    """The exception message should include the file path."""
    path = "example.py"
    exc = FileSkipComment(path)
    assert path in str(exc)
    assert "contains a file skip comment" in str(exc)

def test_file_skip_comment_file_path_attribute():
    """The exception should expose the file_path via its kwargs."""
    path = "module/__init__.py"
    exc = FileSkipComment(path)
    # The base FileSkipped stores kwargs; we expect file_path to be accessible
    assert getattr(exc, "file_path", None) == path

def test_file_skip_comment_inherits_exception():
    """FileSkipComment must be an Exception subclass."""
    path = "test.py"
    exc = FileSkipComment(path)
    assert isinstance(exc, Exception)

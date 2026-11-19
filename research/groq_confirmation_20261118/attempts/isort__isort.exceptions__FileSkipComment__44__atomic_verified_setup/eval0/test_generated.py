import pytest
from isort.exceptions import FileSkipComment


def test_file_skip_comment_initialization():
    """FileSkipComment should store the file path and construct the correct message."""
    file_path = "example.py"
    exc = FileSkipComment(file_path)
    assert exc.file_path == file_path
    assert str(exc) == f"{file_path} contains a file skip comment and was skipped."


def test_file_skip_comment_accepts_additional_kwargs():
    """FileSkipComment should accept arbitrary keyword arguments without error."""
    file_path = "test.py"
    exc = FileSkipComment(file_path, reason="auto", level="high")
    # The base exception should store the message and file_path; kwargs are ignored
    assert exc.file_path == file_path
    assert str(exc) == f"{file_path} contains a file skip comment and was skipped."


def test_file_skip_comment_message_contains_file_path():
    """The exception message must include the provided file path."""
    file_path = "/tmp/some_file.py"
    exc = FileSkipComment(file_path)
    assert file_path in str(exc)

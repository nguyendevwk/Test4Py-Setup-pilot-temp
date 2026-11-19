import pytest
from isort.exceptions import FileSkipComment, FileSkipped


def test_file_skip_comment_message_and_attributes(tmp_path):
    """Verify that the exception message contains the file path and that
    the file_path attribute is correctly set."""
    test_file = tmp_path / "example.py"
    test_file.write_text("# isort: skip_file\n")
    exc = FileSkipComment(str(test_file))
    # The message should mention the file path
    assert str(test_file) in str(exc)
    # The exception should be an instance of FileSkipped
    assert isinstance(exc, FileSkipped)
    # The file_path attribute should be set on the exception
    assert getattr(exc, "file_path") == str(test_file)


def test_file_skip_comment_accepts_additional_kwargs(tmp_path):
    """Ensure that arbitrary keyword arguments are accepted and stored."""
    test_file = tmp_path / "skip.py"
    exc = FileSkipComment(str(test_file), reason="testing", level="debug")
    # The message should still contain the file path
    assert str(test_file) in str(exc)
    # The additional kwargs should be accessible as attributes
    assert getattr(exc, "reason") == "testing"
    assert getattr(exc, "level") == "debug"


def test_file_skip_comment_with_non_string_file_path(tmp_path):
    """Passing a non-string file_path should still work because it is
    converted to a string in the message."""
    test_file = tmp_path / "nonstring.py"
    # Pass an integer instead of a string
    exc = FileSkipComment(42)
    # The message should contain the string representation of the integer
    assert "42" in str(exc)
    # The file_path attribute should also be the string "42"
    assert getattr(exc, "file_path") == "42"

import pytest
from isort.exceptions import FileSkipComment


def test_file_skip_comment_message_and_attribute(tmp_path):
    """The exception should contain the correct message and expose the file_path."""
    file_path = str(tmp_path / "example.py")
    exc = FileSkipComment(file_path)
    expected_msg = f"{file_path} contains a file skip comment and was skipped."
    assert str(exc) == expected_msg
    # The base class should store the file_path in its kwargs
    assert exc.kwargs["file_path"] == file_path


def test_file_skip_comment_accepts_additional_kwargs(tmp_path):
    """Additional keyword arguments should be accepted and stored."""
    file_path = str(tmp_path / "skip.py")
    exc = FileSkipComment(file_path, reason="test", level="debug")
    assert exc.kwargs["file_path"] == file_path
    assert exc.kwargs["reason"] == "test"
    assert exc.kwargs["level"] == "debug"
    # The message should still be based only on the file_path
    assert "contains a file skip comment" in str(exc)


def test_file_skip_comment_is_exception_and_subclass(tmp_path):
    """Ensure the exception behaves like a standard exception and is a subclass of Exception."""
    file_path = str(tmp_path / "skip2.py")
    exc = FileSkipComment(file_path)
    # It should be an instance of Exception
    assert isinstance(exc, Exception)
    # It should be a subclass of FileSkipComment
    assert isinstance(exc, FileSkipComment)
    # Raising and catching should work as expected
    with pytest.raises(FileSkipComment) as excinfo:
        raise exc
    assert excinfo.value is exc

import pytest
from isort.exceptions import FileSkipComment


def test_file_skip_comment_message_and_attribute(tmp_path):
    """Ensure the exception message contains the file path and the attribute is set."""
    file_path = str(tmp_path / "example.py")
    exc = FileSkipComment(file_path)
    expected_msg = f"{file_path} contains a file skip comment and was skipped."
    assert str(exc) == expected_msg
    assert exc.file_path == file_path


def test_file_skip_comment_inherits_from_exception():
    """Verify that FileSkipComment is a subclass of Exception."""
    file_path = "dummy.py"
    exc = FileSkipComment(file_path)
    assert isinstance(exc, Exception)
    assert isinstance(exc, FileSkipComment)


def test_file_skip_comment_with_additional_kwargs(tmp_path):
    """Check that additional keyword arguments are accepted but not stored."""
    file_path = str(tmp_path / "skip.py")
    exc = FileSkipComment(file_path, extra="value")
    # The exception should still have the correct message and file_path
    assert exc.file_path == file_path
    assert "skip.py" in str(exc)
    # The extra keyword should not create a new attribute
    with pytest.raises(AttributeError):
        _ = exc.extra

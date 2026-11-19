import pytest
from isort.exceptions import FileSkipComment, FileSkipped


def test_file_skip_comment_initialization():
    """FileSkipComment should format its message correctly and expose the file_path."""
    path = "example.py"
    exc = FileSkipComment(path, reason="test")
    assert str(exc) == f"{path} contains a file skip comment and was skipped."
    assert exc.file_path == path
    # The custom keyword argument should be stored in the exception's kwargs
    assert exc.kwargs.get("reason") == "test"


def test_file_skip_comment_inherits_file_skipped():
    """FileSkipComment must be an instance of FileSkipped."""
    exc = FileSkipComment("dummy.py")
    assert isinstance(exc, FileSkipped)
    # Ensure that the base class's __init__ was called by checking its message
    assert isinstance(exc, Exception)
    assert "contains a file skip comment" in str(exc)


def test_file_skip_comment_with_multiple_kwargs():
    """All keyword arguments passed to FileSkipComment should be accessible via kwargs."""
    exc = FileSkipComment("module.py", foo="bar", baz=123)
    assert exc.kwargs["foo"] == "bar"
    assert exc.kwargs["baz"] == 123
    # The message should remain unchanged regardless of extra kwargs
    assert str(exc) == "module.py contains a file skip comment and was skipped."

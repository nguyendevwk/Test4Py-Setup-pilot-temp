import pytest
from isort.exceptions import FileSkipComment, FileSkipped
from pathlib import Path


def test_file_skip_comment_message(tmp_path: Path) -> None:
    """FileSkipComment should format its message correctly."""
    file_path = str(tmp_path / "example.py")
    exc = FileSkipComment(file_path)
    expected_msg = f"{file_path} contains a file skip comment and was skipped."
    assert str(exc) == expected_msg
    # The file_path should be stored as an attribute
    assert getattr(exc, "file_path") == file_path


def test_file_skip_comment_inheritance() -> None:
    """FileSkipComment must be a subclass of FileSkipped."""
    assert issubclass(FileSkipComment, FileSkipped)
    # Instantiating should not raise
    exc = FileSkipComment("dummy.py")
    assert isinstance(exc, FileSkipped)


def test_file_skip_comment_with_extra_kwargs(tmp_path: Path) -> None:
    """Extra keyword arguments should be accepted and stored."""
    file_path = str(tmp_path / "skip.py")
    exc = FileSkipComment(file_path, reason="test", level="debug")
    # The message should still be correct
    assert str(exc) == f"{file_path} contains a file skip comment and was skipped."
    # Extra kwargs should be accessible via the exception's __dict__
    assert exc.__dict__["reason"] == "test"
    assert exc.__dict__["level"] == "debug"

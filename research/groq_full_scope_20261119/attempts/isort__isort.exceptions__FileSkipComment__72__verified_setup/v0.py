import pytest
from pathlib import Path
from isort.exceptions import FileSkipComment, FileSkipped


def test_file_skip_comment_message_and_attribute(tmp_path: Path):
    """Normal instantiation should set the message and file_path attribute correctly."""
    file_path = str(tmp_path / "example.py")
    exc = FileSkipComment(file_path)
    # The exception message should contain the file path
    assert file_path in str(exc)
    # The file_path attribute should be stored on the exception
    assert getattr(exc, "file_path") == file_path
    # It should be an instance of FileSkipped
    assert isinstance(exc, FileSkipped)


def test_file_skip_comment_with_empty_path(tmp_path: Path):
    """An empty string as file_path should still produce a valid exception."""
    file_path = ""
    exc = FileSkipComment(file_path)
    # The message should still be constructed without raising
    assert str(exc) == f"{file_path} contains a file skip comment and was skipped."
    # The file_path attribute should be the empty string
    assert getattr(exc, "file_path") == file_path


def test_file_skip_comment_invalid_type_raises():
    """Passing a non-string type should raise a TypeError due to type checking."""
    with pytest.raises(TypeError):
        FileSkipComment(123)  # type: ignore[arg-type]

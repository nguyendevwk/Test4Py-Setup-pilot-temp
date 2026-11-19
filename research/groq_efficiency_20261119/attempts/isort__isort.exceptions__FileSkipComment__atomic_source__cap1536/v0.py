import pytest
from isort.exceptions import FileSkipComment


def test_file_skip_comment_initialization(tmp_path):
    """FileSkipComment should store the file path and format the message correctly."""
    file_path = str(tmp_path / "example.py")
    exc = FileSkipComment(file_path, extra="ignored")
    # The message should mention the file path
    assert file_path in str(exc)
    # The file_path attribute should be accessible
    assert getattr(exc, "file_path") == file_path
    # The exception should be an instance of Exception
    assert isinstance(exc, Exception)


def test_file_skip_comment_inherits_from_file_skipped(tmp_path):
    """FileSkipComment should inherit from FileSkipped."""
    from isort.exceptions import FileSkipped

    file_path = str(tmp_path / "skip.py")
    exc = FileSkipComment(file_path)
    # Ensure the type hierarchy is correct
    assert isinstance(exc, FileSkipped)
    assert isinstance(exc, Exception)


def test_file_skip_comment_raises_and_catches(tmp_path):
    """Raising FileSkipComment should propagate correctly and be caught."""
    file_path = str(tmp_path / "to_skip.py")

    with pytest.raises(FileSkipComment) as excinfo:
        raise FileSkipComment(file_path)

    # The caught exception should have the same file_path
    assert excinfo.value.file_path == file_path
    # The message should be exactly as defined in the constructor
    expected_msg = f"{file_path} contains a file skip comment and was skipped."
    assert str(excinfo.value) == expected_msg

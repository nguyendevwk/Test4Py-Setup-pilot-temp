import pytest
from isort.exceptions import FileSkipComment

def test_file_skip_comment_initialization(tmp_path):
    """Verify that FileSkipComment stores the file path and constructs the correct message."""
    file_path = str(tmp_path / "example.py")
    exc = FileSkipComment(file_path)
    assert isinstance(exc, Exception)
    assert exc.file_path == file_path
    expected_msg = f"{file_path} contains a file skip comment and was skipped."
    assert str(exc) == expected_msg

def test_file_skip_comment_inherits_from_file_skipped(tmp_path):
    """Ensure FileSkipComment is a subclass of FileSkipped."""
    file_path = str(tmp_path / "skip.py")
    exc = FileSkipComment(file_path)
    # The base class is not directly importable, but we can check the MRO for the name
    mro_names = [cls.__name__ for cls in exc.__class__.__mro__]
    assert "FileSkipped" in mro_names

def test_file_skip_comment_raises_and_catches(tmp_path):
    """Test that raising FileSkipComment propagates correctly and can be caught."""
    file_path = str(tmp_path / "raise.py")
    with pytest.raises(FileSkipComment) as excinfo:
        raise FileSkipComment(file_path)
    caught = excinfo.value
    assert caught.file_path == file_path
    assert "contains a file skip comment" in str(caught)

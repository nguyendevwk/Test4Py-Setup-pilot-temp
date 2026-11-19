import pytest
from isort.exceptions import FileSkipComment, FileSkipped, ISortError


def test_file_skip_comment_initialization_and_attributes(tmp_path):
    """Verify that FileSkipComment stores the file path and constructs the correct message."""
    file_path = str(tmp_path / "example.py")
    exc = FileSkipComment(file_path)
    # The message should contain the file path and the skip notice
    assert file_path in exc.message
    assert "skipped" in exc.message
    # The file_path attribute should be preserved
    assert exc.file_path == file_path
    # It should be an instance of FileSkipped and ISortError
    assert isinstance(exc, FileSkipped)
    assert isinstance(exc, ISortError)


def test_file_skip_comment_inherits_from_file_skipped():
    """Ensure that FileSkipComment is a subclass of FileSkipped."""
    file_path = "/dev/null"
    exc = FileSkipComment(file_path)
    # Direct subclass check
    assert isinstance(exc, FileSkipped)
    # The base class constructor should have been called with the correct message
    expected_msg = f"{file_path} contains a file skip comment and was skipped."
    assert exc.message == expected_msg
    # The file_path attribute should match the argument
    assert exc.file_path == file_path


def test_file_skip_comment_raises_with_invalid_input():
    """FileSkipComment should raise a TypeError when called with non-string file_path."""
    with pytest.raises(TypeError):
        # Passing an integer should trigger a TypeError due to type mismatch
        FileSkipComment(123)  # type: ignore[arg-type]

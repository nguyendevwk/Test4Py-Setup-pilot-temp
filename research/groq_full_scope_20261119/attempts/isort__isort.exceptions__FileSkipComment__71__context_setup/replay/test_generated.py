import pytest
from isort.exceptions import FileSkipComment, FileSkipped, ISortError


def test_file_skip_comment_message_and_attributes():
    """FileSkipComment should store the file path and include it in the message."""
    file_path = "example.py"
    exc = FileSkipComment(file_path)
    # The message should mention the file path
    assert file_path in exc.args[0]
    # The file_path attribute should be set correctly
    assert exc.file_path == file_path
    # The message attribute should match the first argument
    assert exc.message == exc.args[0]


def test_file_skip_comment_inheritance():
    """FileSkipComment must inherit from FileSkipped and ISortError."""
    file_path = "test.py"
    exc = FileSkipComment(file_path)
    # Direct subclass of FileSkipped
    assert isinstance(exc, FileSkipped)
    # Indirect subclass of ISortError through FileSkipped
    assert isinstance(exc, ISortError)
    # Ensure the MRO includes the expected classes
    assert FileSkipped in exc.__class__.__mro__
    assert ISortError in exc.__class__.__mro__


def test_file_skip_comment_raised_and_caught():
    """Raising FileSkipComment should propagate correctly and be caught as ISortError."""
    file_path = "skip_this.py"
    with pytest.raises(ISortError) as excinfo:
        raise FileSkipComment(file_path)
    # The caught exception should be the same instance
    assert isinstance(excinfo.value, FileSkipComment)
    assert excinfo.value.file_path == file_path
    # The message should be present in the exception string
    assert file_path in str(excinfo.value)

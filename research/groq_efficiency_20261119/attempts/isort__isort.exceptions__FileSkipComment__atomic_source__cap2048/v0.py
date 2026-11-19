import pytest
from isort.exceptions import FileSkipComment

def test_file_skip_comment_initialization():
    """Verify that FileSkipComment stores the file path and constructs the correct message."""
    path = "example.py"
    exc = FileSkipComment(path)
    assert isinstance(exc, FileSkipComment)
    assert exc.file_path == path
    expected_msg = f"{path} contains a file skip comment and was skipped."
    assert str(exc) == expected_msg

def test_file_skip_comment_inherits_exception():
    """Ensure FileSkipComment is a subclass of Exception and can be caught as such."""
    path = "skip.py"
    exc = FileSkipComment(path)
    try:
        raise exc
    except FileSkipComment as e:
        assert isinstance(e, Exception)
        assert e.file_path == path
    else:
        pytest.fail("FileSkipComment was not caught by its own except clause")

def test_file_skip_comment_message_consistency():
    """Check that the message remains consistent across multiple accesses."""
    path = "test_file.py"
    exc = FileSkipComment(path)
    first_str = str(exc)
    second_str = exc.args[0]
    assert first_str == second_str
    assert path in first_str

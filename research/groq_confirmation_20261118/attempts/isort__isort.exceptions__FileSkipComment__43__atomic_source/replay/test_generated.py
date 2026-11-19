import pytest
from isort.exceptions import FileSkipComment

# Test that FileSkipComment is a subclass of Exception and FileSkipped
def test_file_skip_comment_inheritance():
    assert issubclass(FileSkipComment, Exception)
    # The base class FileSkipped is defined in the same module
    from isort.exceptions import FileSkipped
    assert issubclass(FileSkipComment, FileSkipped)

# Test that the error message contains the provided file path
def test_file_skip_comment_message(tmp_path):
    file_path = tmp_path / "example.py"
    file_path.write_text("# isort: skip_file\n")
    exc = FileSkipComment(str(file_path))
    expected_msg = f"{file_path} contains a file skip comment and was skipped."
    assert str(exc) == expected_msg
    # The file_path attribute should be stored on the exception
    assert exc.file_path == str(file_path)

# Test that FileSkipComment can be raised and caught correctly
def test_file_skip_comment_raise_and_catch(tmp_path):
    file_path = tmp_path / "skip.py"
    file_path.write_text("# isort: skip_file\n")
    try:
        raise FileSkipComment(str(file_path))
    except FileSkipComment as e:
        assert e.file_path == str(file_path)
        assert "contains a file skip comment" in str(e)
    else:
        pytest.fail("FileSkipComment was not raised")

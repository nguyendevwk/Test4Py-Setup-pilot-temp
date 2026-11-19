import pytest
from isort.exceptions import FileSkipSetting


def test_file_skip_setting_message_and_attributes(tmp_path):
    """Verify that the exception message contains the file path and the
    custom attributes are set correctly."""
    file_path = str(tmp_path / "example.py")
    exc = FileSkipSetting(file_path)
    # The message should mention the file path
    assert file_path in str(exc)
    # The exception should expose the file_path attribute
    assert hasattr(exc, "file_path")
    assert exc.file_path == file_path
    # The exception should be an instance of Exception
    assert isinstance(exc, Exception)


def test_file_skip_setting_raises_and_catches():
    """Ensure that raising the exception propagates correctly and can be
    caught with the expected type."""
    file_path = "/tmp/nonexistent.py"
    with pytest.raises(FileSkipSetting) as excinfo:
        raise FileSkipSetting(file_path)
    # The caught exception should have the same file_path
    assert excinfo.value.file_path == file_path
    # The message should contain the file path
    assert file_path in str(excinfo.value)


def test_file_skip_setting_inherits_from_base_exception():
    """Confirm that FileSkipSetting inherits from the base FileSkipped
    exception class defined in isort.exceptions."""
    from isort.exceptions import FileSkipped
    file_path = "dummy.py"
    exc = FileSkipSetting(file_path)
    # It should be an instance of FileSkipped
    assert isinstance(exc, FileSkipped)
    # And also an instance of Exception
    assert isinstance(exc, Exception)

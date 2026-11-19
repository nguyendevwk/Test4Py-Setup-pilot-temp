import pytest
from isort.exceptions import FileSkipSetting


def test_file_skip_setting_message_contains_path():
    """The exception message should include the provided file path."""
    file_path = "example.py"
    exc = FileSkipSetting(file_path)
    assert file_path in str(exc), "Message does not contain the file path"
    assert (
        f"{file_path} was skipped" in str(exc)
    ), "Message does not start with expected prefix"


def test_file_skip_setting_stores_file_path_attribute():
    """The exception should expose the file_path attribute."""
    file_path = "/tmp/some/file.py"
    exc = FileSkipSetting(file_path)
    assert hasattr(exc, "file_path"), "Exception missing file_path attribute"
    assert exc.file_path == file_path, "file_path attribute value incorrect"


def test_file_skip_setting_accepts_additional_kwargs():
    """Providing additional keyword arguments should not alter the exception."""
    file_path = "skip_me.py"
    extra = {"reason": "test", "code": 123}
    exc = FileSkipSetting(file_path, **extra)
    # The message should still be correct
    assert file_path in str(exc)
    # The extra kwargs should not be stored as attributes
    for key in extra:
        assert not hasattr(exc, key), f"Unexpected attribute {key} found"

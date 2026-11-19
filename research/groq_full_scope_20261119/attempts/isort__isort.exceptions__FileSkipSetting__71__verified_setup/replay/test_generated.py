import pytest
from isort.exceptions import FileSkipSetting, FileSkipped


def test_file_skip_setting_message_and_attributes(tmp_path):
    """FileSkipSetting should construct the correct message and store the file path."""
    file_path = str(tmp_path / "example.py")
    exc = FileSkipSetting(file_path)
    # The message should mention the file path and the skip reason
    assert file_path in str(exc)
    assert "was skipped as it's listed in 'skip' setting" in str(exc)
    # The exception should expose the file_path attribute
    assert hasattr(exc, "file_path")
    assert exc.file_path == file_path


def test_file_skip_setting_inherits_file_skipped():
    """FileSkipSetting must be a subclass of FileSkipped."""
    exc = FileSkipSetting("dummy.py")
    assert isinstance(exc, FileSkipped)
    # FileSkipped should be the direct base class
    assert FileSkipped in exc.__class__.__mro__


def test_file_skip_setting_accepts_additional_kwargs(tmp_path):
    """Passing unexpected keyword arguments should not alter the exception behavior."""
    file_path = str(tmp_path / "dummy.py")
    # Provide an arbitrary keyword argument
    exc = FileSkipSetting(file_path, extra="value")
    # The message and file_path should remain unchanged
    assert file_path in str(exc)
    assert exc.file_path == file_path
    # No AttributeError should be raised for the extra keyword
    assert getattr(exc, "extra", None) is None

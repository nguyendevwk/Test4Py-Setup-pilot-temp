import pytest
from isort.exceptions import FileSkipSetting, FileSkipped, ISortError


def test_file_skip_setting_initialization_and_attributes():
    """Verify that FileSkipSetting stores the file path and constructs the correct message."""
    file_path = "example.py"
    exc = FileSkipSetting(file_path)
    assert isinstance(exc, FileSkipSetting)
    assert isinstance(exc, FileSkipped)
    assert isinstance(exc, ISortError)
    expected_msg = (
        f"{file_path} was skipped as it's listed in 'skip' setting"
        " or matches a glob in 'skip_glob' setting"
    )
    assert exc.args[0] == expected_msg
    assert exc.message == expected_msg
    assert exc.file_path == file_path


def test_file_skip_setting_with_additional_kwargs():
    """Ensure that additional keyword arguments are accepted but ignored in the message."""
    file_path = "skip_me.py"
    exc = FileSkipSetting(file_path, reason="ignored", extra="data")
    assert exc.file_path == file_path
    # The message should not contain the extra kwargs
    assert "ignored" not in exc.args[0]
    assert "data" not in exc.args[0]
    # The kwargs should not be stored as attributes
    assert not hasattr(exc, "reason")
    assert not hasattr(exc, "extra")


def test_file_skip_setting_message_consistency():
    """Check that the message format remains consistent across different file paths."""
    paths = ["a.py", "b.py", "c.py"]
    messages = [FileSkipSetting(p).args[0] for p in paths]
    # All messages should be identical except for the file name
    base_msg = (
        " was skipped as it's listed in 'skip' setting"
        " or matches a glob in 'skip_glob' setting"
    )
    for p, msg in zip(paths, messages):
        assert msg == f"{p}{base_msg}"

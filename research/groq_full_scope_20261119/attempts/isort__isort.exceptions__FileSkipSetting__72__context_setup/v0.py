import pytest
from isort.exceptions import FileSkipSetting, FileSkipped, ISortError


def test_file_skip_setting_initialization_and_attributes(tmp_path):
    """FileSkipSetting should store the file path and construct the correct message."""
    test_file = tmp_path / "example.py"
    exc = FileSkipSetting(str(test_file))
    # The message should mention the file path and the skip reason
    assert str(test_file) in exc.args[0]
    assert "was skipped as it's listed in 'skip' setting" in exc.args[0]
    # The file_path attribute should be set correctly
    assert exc.file_path == str(test_file)
    # The message attribute from FileSkipped should match the args[0]
    assert exc.message == exc.args[0]


def test_file_skip_setting_inheritance_and_type():
    """FileSkipSetting must inherit from FileSkipped and ISortError."""
    exc = FileSkipSetting("dummy.py")
    # Direct subclass checks
    assert isinstance(exc, FileSkipped)
    assert isinstance(exc, ISortError)
    # Ensure the base Exception class is also in the MRO
    assert isinstance(exc, Exception)


def test_file_skip_setting_ignores_extra_kwargs():
    """Extra keyword arguments passed to FileSkipSetting should be ignored."""
    exc = FileSkipSetting("dummy.py", extra="ignored", another="value")
    # The exception should still be constructed correctly
    assert exc.file_path == "dummy.py"
    assert "was skipped" in exc.args[0]
    # No unexpected attributes should be added
    with pytest.raises(AttributeError):
        _ = exc.extra
    with pytest.raises(AttributeError):
        _ = exc.another

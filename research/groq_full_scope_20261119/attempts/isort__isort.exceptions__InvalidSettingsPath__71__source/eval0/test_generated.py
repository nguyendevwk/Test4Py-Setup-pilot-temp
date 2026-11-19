import pytest
from pathlib import Path
from isort.exceptions import InvalidSettingsPath

def test_invalid_settings_path_message_with_str():
    """The exception message should include the string path provided."""
    path_str = "nonexistent/path"
    exc = InvalidSettingsPath(path_str)
    assert isinstance(exc, InvalidSettingsPath)
    assert exc.settings_path == path_str
    assert f"{path_str}" in str(exc)
    assert "does not exist" in str(exc)

def test_invalid_settings_path_message_with_path_object(tmp_path):
    """The exception should accept a Path object and store it correctly."""
    # Create a temporary path that does not exist
    non_existent = tmp_path / "does_not_exist"
    exc = InvalidSettingsPath(non_existent)
    assert isinstance(exc, InvalidSettingsPath)
    assert exc.settings_path == non_existent
    # The string representation should use the Path's string form
    assert str(non_existent) in str(exc)
    assert "does not exist" in str(exc)

def test_invalid_settings_path_inherits_from_ISortError():
    """Ensure that InvalidSettingsPath is a subclass of ISortError."""
    from isort.exceptions import ISortError
    path = "missing"
    exc = InvalidSettingsPath(path)
    assert isinstance(exc, ISortError)
    # The base class message should be preserved
    assert isinstance(exc.args[0], str)
    assert "isort was told to use the settings_path" in exc.args[0]

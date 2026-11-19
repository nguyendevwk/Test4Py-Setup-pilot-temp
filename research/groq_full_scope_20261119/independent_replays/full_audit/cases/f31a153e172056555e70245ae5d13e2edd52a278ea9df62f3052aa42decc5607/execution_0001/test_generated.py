import pytest
from pathlib import Path
from isort.exceptions import InvalidSettingsPath, ISortError


def test_invalid_settings_path_initialization_with_string():
    """Creating an InvalidSettingsPath with a non‑existent string path should store the path."""
    path_str = "nonexistent/path"
    exc = InvalidSettingsPath(path_str)
    assert isinstance(exc, ISortError)
    assert exc.settings_path == path_str
    assert "nonexistent/path" in str(exc)


def test_invalid_settings_path_initialization_with_path_object(tmp_path):
    """Creating an InvalidSettingsPath with a Path object should preserve the Path."""
    nonexistent = tmp_path / "does_not_exist"
    exc = InvalidSettingsPath(nonexistent)
    assert isinstance(exc, ISortError)
    assert exc.settings_path == nonexistent
    assert str(nonexistent) in str(exc)


def test_invalid_settings_path_message_format(tmp_path):
    """The error message should clearly state the missing path and use the correct wording."""
    missing = tmp_path / "missing"
    exc = InvalidSettingsPath(missing)
    msg = str(exc)
    assert "isort was told to use the settings_path" in msg
    assert str(missing) in msg
    assert "does not exist" in msg

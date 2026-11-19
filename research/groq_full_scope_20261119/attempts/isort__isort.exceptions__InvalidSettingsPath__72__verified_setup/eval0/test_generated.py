import pytest
from pathlib import Path
from isort.exceptions import InvalidSettingsPath, ISortError


def test_invalid_settings_path_message_contains_path(tmp_path: Path):
    """The error message should include the provided path."""
    non_existent = tmp_path / "does_not_exist.cfg"
    exc = InvalidSettingsPath(non_existent)
    assert str(non_existent) in str(exc)
    assert "does_not_exist.cfg" in str(exc)


def test_invalid_settings_path_stores_path_attribute(tmp_path: Path):
    """The settings_path attribute should be set to the original argument."""
    path = tmp_path / "config.ini"
    exc = InvalidSettingsPath(path)
    assert exc.settings_path == path


def test_invalid_settings_path_is_subclass_of_ISortError(tmp_path: Path):
    """InvalidSettingsPath should be an instance of ISortError."""
    path = Path("some/path")
    exc = InvalidSettingsPath(path)
    assert isinstance(exc, ISortError)

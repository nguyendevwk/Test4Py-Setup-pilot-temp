import pytest
from pathlib import Path
from isort.exceptions import InvalidSettingsPath


def test_invalid_settings_path_message_with_str(tmp_path: Path):
    """When constructed with a string path that does not exist,
    the exception message should mention the provided path."""
    non_existent = tmp_path / "does_not_exist.cfg"
    exc = InvalidSettingsPath(str(non_existent))
    assert str(non_existent) in str(exc)
    assert "does not exist" in str(exc)


def test_invalid_settings_path_message_with_path(tmp_path: Path):
    """When constructed with a Path object that does not exist,
    the exception message should mention the provided path."""
    non_existent = tmp_path / "missing.ini"
    exc = InvalidSettingsPath(non_existent)
    assert str(non_existent) in str(exc)
    assert "does not exist" in str(exc)


def test_invalid_settings_path_attribute(tmp_path: Path):
    """The settings_path attribute should store the original argument."""
    non_existent = tmp_path / "config.toml"
    exc = InvalidSettingsPath(non_existent)
    assert exc.settings_path == non_existent

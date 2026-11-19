import pytest
from pathlib import Path
from isort.exceptions import InvalidSettingsPath, ISortError


def test_invalid_settings_path_message(tmp_path: Path):
    """The exception message should include the provided path string."""
    non_existent = tmp_path / "does_not_exist.cfg"
    exc = InvalidSettingsPath(non_existent)
    # The message should mention the path in its string representation
    assert str(non_existent) in str(exc)
    # The message should start with the expected prefix
    assert str(exc).startswith(
        "isort was told to use the settings_path: "
    )


def test_invalid_settings_path_attribute(tmp_path: Path):
    """The exception should store the original path in the settings_path attribute."""
    non_existent = tmp_path / "missing.ini"
    exc = InvalidSettingsPath(non_existent)
    # The attribute should be the same object passed in
    assert exc.settings_path is non_existent
    # And its string representation should match
    assert str(exc.settings_path) == str(non_existent)


def test_invalid_settings_path_inherits_exception(tmp_path: Path):
    """InvalidSettingsPath should be a subclass of ISortError and Exception."""
    non_existent = tmp_path / "config.json"
    exc = InvalidSettingsPath(non_existent)
    # It should be an instance of ISortError
    assert isinstance(exc, ISortError)
    # And also an instance of the built‑in Exception
    assert isinstance(exc, Exception)

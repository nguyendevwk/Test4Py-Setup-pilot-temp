import pytest
from pathlib import Path
from isort.exceptions import InvalidSettingsPath, ISortError


def test_invalid_settings_path_message_and_attribute(tmp_path: Path):
    """The exception should store the provided path and format its message correctly."""
    # Create a path that does not exist
    non_existent = tmp_path / "does_not_exist.cfg"
    # Instantiate the exception
    exc = InvalidSettingsPath(non_existent)
    # The settings_path attribute should be the original Path object
    assert exc.settings_path == non_existent
    # The message should mention the path string representation
    assert str(non_existent) in str(exc)
    # The message should start with the expected prefix
    assert str(exc).startswith("isort was told to use the settings_path:")


def test_invalid_settings_path_inherits_isort_error():
    """InvalidSettingsPath must be a subclass of ISortError."""
    # Use a simple string path that does not exist
    exc = InvalidSettingsPath("nonexistent_path")
    # Ensure the exception is an instance of ISortError
    assert isinstance(exc, ISortError)


def test_invalid_settings_path_raises_with_string_and_path(tmp_path: Path):
    """The exception should accept both str and Path inputs and raise consistently."""
    # Path input
    path_input = tmp_path / "missing_file.py"
    exc_path = InvalidSettingsPath(path_input)
    assert exc_path.settings_path == path_input
    # String input
    str_input = "another_missing_file.py"
    exc_str = InvalidSettingsPath(str_input)
    assert exc_str.settings_path == str_input
    # The messages should contain the respective inputs
    assert str_input in str(exc_str)
    assert str(path_input) in str(exc_path)

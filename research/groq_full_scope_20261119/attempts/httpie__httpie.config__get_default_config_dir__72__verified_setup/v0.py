import os
import sys
from pathlib import Path

import pytest

# Import the target function
from httpie.config import get_default_config_dir, ENV_HTTPIE_CONFIG_DIR, ENV_XDG_CONFIG_HOME, DEFAULT_RELATIVE_LEGACY_CONFIG_DIR, DEFAULT_CONFIG_DIRNAME, DEFAULT_RELATIVE_XDG_CONFIG_HOME, DEFAULT_WINDOWS_CONFIG_DIR, is_windows


def test_env_var_overrides_all(tmp_path, monkeypatch):
    """When HTTPIE_CONFIG_DIR is set, it takes precedence over everything else."""
    # Set the environment variable to a temporary directory
    env_dir = tmp_path / "env_config"
    env_dir.mkdir()
    monkeypatch.setenv(ENV_HTTPIE_CONFIG_DIR, str(env_dir))

    # Ensure other conditions are false
    monkeypatch.delenv(ENV_XDG_CONFIG_HOME, raising=False)
    monkeypatch.setattr(Path, "home", lambda: tmp_path / "home")
    monkeypatch.setattr(is_windows, "__call__", lambda: False)

    # Call the function
    result = get_default_config_dir()

    # Assert that the returned path is exactly the env var path
    assert result == env_dir
    assert result.is_absolute()


def test_legacy_config_dir_exists(tmp_path, monkeypatch):
    """If the legacy ~/.httpie directory exists, it is returned."""
    # Simulate a home directory
    home_dir = tmp_path / "home"
    home_dir.mkdir()
    # Create the legacy config directory
    legacy_dir = home_dir / DEFAULT_RELATIVE_LEGACY_CONFIG_DIR
    legacy_dir.mkdir()

    # Ensure env var is not set
    monkeypatch.delenv(ENV_HTTPIE_CONFIG_DIR, raising=False)
    # Ensure XDG env var is not set
    monkeypatch.delenv(ENV_XDG_CONFIG_HOME, raising=False)
    # Patch Path.home to return our fake home
    monkeypatch.setattr(Path, "home", lambda: home_dir)
    # Ensure not on Windows
    monkeypatch.setattr(is_windows, "__call__", lambda: False)

    # Call the function
    result = get_default_config_dir()

    # Assert that the legacy directory is returned
    assert result == legacy_dir
    assert result.is_dir()


def test_xdg_default_when_no_env_or_legacy(tmp_path, monkeypatch):
    """When no env var or legacy directory, XDG default is used."""
    # Simulate a home directory without legacy config
    home_dir = tmp_path / "home"
    home_dir.mkdir()

    # Ensure env var is not set
    monkeypatch.delenv(ENV_HTTPIE_CONFIG_DIR, raising=False)
    # Ensure XDG env var is not set
    monkeypatch.delenv(ENV_XDG_CONFIG_HOME, raising=False)
    # Patch Path.home to return our fake home
    monkeypatch.setattr(Path, "home", lambda: home_dir)
    # Ensure not on Windows
    monkeypatch.setattr(is_windows, "__call__", lambda: False)

    # Call the function
    result = get_default_config_dir()

    # Expected path: $HOME/.config/httpie
    expected = home_dir / DEFAULT_RELATIVE_XDG_CONFIG_HOME / DEFAULT_CONFIG_DIRNAME
    assert result == expected
    assert result.is_absolute()

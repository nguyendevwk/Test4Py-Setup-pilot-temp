import os
import sys
from pathlib import Path

import pytest

# Import the target function from the production code
from httpie.config import get_default_config_dir, ENV_HTTPIE_CONFIG_DIR, ENV_XDG_CONFIG_HOME, DEFAULT_RELATIVE_LEGACY_CONFIG_DIR, DEFAULT_CONFIG_DIRNAME, DEFAULT_WINDOWS_CONFIG_DIR, is_windows


def test_env_override(tmp_path, monkeypatch):
    """When ENV_HTTPIE_CONFIG_DIR is set, the function returns that path."""
    custom_dir = tmp_path / "custom_config"
    monkeypatch.setenv(ENV_HTTPIE_CONFIG_DIR, str(custom_dir))
    # Ensure the path is not created to test pure env override
    assert not custom_dir.exists()
    result = get_default_config_dir()
    assert result == custom_dir
    # Clean up environment variable
    monkeypatch.delenv(ENV_HTTPIE_CONFIG_DIR, raising=False)


def test_legacy_config_dir_exists(tmp_path, monkeypatch):
    """If a legacy ~/.httpie directory exists, it is returned."""
    # Create a fake home directory
    fake_home = tmp_path / "home"
    fake_home.mkdir()
    # Create the legacy config directory inside the fake home
    legacy_dir = fake_home / DEFAULT_RELATIVE_LEGACY_CONFIG_DIR
    legacy_dir.mkdir()
    # Patch Path.home to return our fake home
    monkeypatch.setattr(Path, "home", lambda: fake_home)
    # Ensure no environment variables interfere
    monkeypatch.delenv(ENV_HTTPIE_CONFIG_DIR, raising=False)
    monkeypatch.delenv(ENV_XDG_CONFIG_HOME, raising=False)
    result = get_default_config_dir()
    assert result == legacy_dir


def test_xdg_default(tmp_path, monkeypatch):
    """When no legacy dir and no env vars, XDG default is used."""
    # Create a fake home directory
    fake_home = tmp_path / "home"
    fake_home.mkdir()
    # Ensure legacy dir does not exist
    legacy_dir = fake_home / DEFAULT_RELATIVE_LEGACY_CONFIG_DIR
    assert not legacy_dir.exists()
    # Patch Path.home to return our fake home
    monkeypatch.setattr(Path, "home", lambda: fake_home)
    # Ensure no environment variables interfere
    monkeypatch.delenv(ENV_HTTPIE_CONFIG_DIR, raising=False)
    monkeypatch.delenv(ENV_XDG_CONFIG_HOME, raising=False)
    # Compute expected XDG path
    expected = Path(fake_home / DEFAULT_RELATIVE_XDG_CONFIG_HOME) / DEFAULT_CONFIG_DIRNAME
    result = get_default_config_dir()
    assert result == expected

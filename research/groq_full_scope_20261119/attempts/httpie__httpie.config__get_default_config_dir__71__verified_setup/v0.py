import os
import shutil
from pathlib import Path

import pytest

from httpie.config import get_default_config_dir, ENV_HTTPIE_CONFIG_DIR, ENV_XDG_CONFIG_HOME, DEFAULT_RELATIVE_LEGACY_CONFIG_DIR, DEFAULT_CONFIG_DIRNAME, DEFAULT_RELATIVE_XDG_CONFIG_HOME, DEFAULT_WINDOWS_CONFIG_DIR, is_windows


def test_env_var_overrides_all(monkeypatch, tmp_path):
    """When ENV_HTTPIE_CONFIG_DIR is set, its value is returned regardless of other factors."""
    custom_dir = tmp_path / "custom_config"
    custom_dir.mkdir()
    monkeypatch.setenv(ENV_HTTPIE_CONFIG_DIR, str(custom_dir))
    # Ensure other conditions would otherwise pick a different dir
    monkeypatch.delenv(ENV_XDG_CONFIG_HOME, raising=False)
    monkeypatch.setattr(Path, "home", lambda: tmp_path / "home")
    monkeypatch.setattr(is_windows, "__call__", lambda: False)
    # Legacy dir exists
    legacy = tmp_path / "home" / DEFAULT_RELATIVE_LEGACY_CONFIG_DIR
    legacy.mkdir(parents=True)
    # XDG default exists
    xdg = tmp_path / "home" / DEFAULT_RELATIVE_XDG_CONFIG_HOME
    xdg.mkdir(parents=True)
    # Call function
    result = get_default_config_dir()
    assert result == custom_dir, f"Expected {custom_dir}, got {result}"


def test_legacy_dir_exists(monkeypatch, tmp_path):
    """If legacy ~/.httpie exists, it is returned when no env var is set."""
    # No env var
    monkeypatch.delenv(ENV_HTTPIE_CONFIG_DIR, raising=False)
    # Set home to tmp_path
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    # Ensure not Windows
    monkeypatch.setattr(is_windows, "__call__", lambda: False)
    # Create legacy dir
    legacy = tmp_path / DEFAULT_RELATIVE_LEGACY_CONFIG_DIR
    legacy.mkdir()
    # Ensure XDG dir does not exist
    xdg = tmp_path / DEFAULT_RELATIVE_XDG_CONFIG_HOME
    if xdg.exists():
        shutil.rmtree(xdg)
    # Call function
    result = get_default_config_dir()
    assert result == legacy, f"Expected legacy dir {legacy}, got {result}"


def test_xdg_default_when_no_legacy(monkeypatch, tmp_path):
    """When no legacy dir and no env var, XDG default is used."""
    # No env var
    monkeypatch.delenv(ENV_HTTPIE_CONFIG_DIR, raising=False)
    # Set home to tmp_path
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    # Ensure not Windows
    monkeypatch.setattr(is_windows, "__call__", lambda: False)
    # Ensure legacy dir does not exist
    legacy = tmp_path / DEFAULT_RELATIVE_LEGACY_CONFIG_DIR
    if legacy.exists():
        shutil.rmtree(legacy)
    # Ensure XDG config home is not set
    monkeypatch.delenv(ENV_XDG_CONFIG_HOME, raising=False)
    # Call function
    result = get_default_config_dir()
    expected = tmp_path / DEFAULT_RELATIVE_XDG_CONFIG_HOME / DEFAULT_CONFIG_DIRNAME
    assert result == expected, f"Expected XDG default {expected}, got {result}"

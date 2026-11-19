import os
import shutil
import sys
from pathlib import Path

import pytest

# Import the target function after setting up the environment
from httpie.config import get_default_config_dir, DEFAULT_CONFIG_DIRNAME, DEFAULT_RELATIVE_LEGACY_CONFIG_DIR, DEFAULT_RELATIVE_XDG_CONFIG_HOME, ENV_HTTPIE_CONFIG_DIR, ENV_XDG_CONFIG_HOME


def test_env_override_config_dir(tmp_path, monkeypatch):
    """When HTTPIE_CONFIG_DIR is set, it overrides all other logic."""
    override_dir = tmp_path / "override"
    override_dir.mkdir()
    monkeypatch.setenv(ENV_HTTPIE_CONFIG_DIR, str(override_dir))
    # Ensure other env vars are unset
    monkeypatch.delenv(ENV_XDG_CONFIG_HOME, raising=False)
    # Ensure home is not used
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    result = get_default_config_dir()
    assert result == override_dir
    assert result.is_absolute()


def test_legacy_config_dir_exists(tmp_path, monkeypatch):
    """If a legacy ~/.httpie directory exists, it is returned."""
    # Set HOME to tmp_path
    monkeypatch.setenv("HOME", str(tmp_path))
    # Ensure HTTPIE_CONFIG_DIR is not set
    monkeypatch.delenv(ENV_HTTPIE_CONFIG_DIR, raising=False)
    # Create legacy directory
    legacy_dir = tmp_path / DEFAULT_RELATIVE_LEGACY_CONFIG_DIR
    legacy_dir.mkdir()
    result = get_default_config_dir()
    assert result == legacy_dir
    assert result.is_absolute()


def test_xdg_default_config_dir(tmp_path, monkeypatch):
    """When no legacy dir and no env override, XDG config dir is used."""
    # Set HOME to tmp_path
    monkeypatch.setenv("HOME", str(tmp_path))
    # Ensure HTTPIE_CONFIG_DIR is not set
    monkeypatch.delenv(ENV_HTTPIE_CONFIG_DIR, raising=False)
    # Ensure legacy dir does not exist
    legacy_dir = tmp_path / DEFAULT_RELATIVE_LEGACY_CONFIG_DIR
    if legacy_dir.exists():
        shutil.rmtree(legacy_dir)
    # Set XDG_CONFIG_HOME to a custom path
    xdg_home = tmp_path / "xdg"
    xdg_home.mkdir()
    monkeypatch.setenv(ENV_XDG_CONFIG_HOME, str(xdg_home))
    result = get_default_config_dir()
    expected = xdg_home / DEFAULT_CONFIG_DIRNAME
    assert result == expected
    assert result.is_absolute()

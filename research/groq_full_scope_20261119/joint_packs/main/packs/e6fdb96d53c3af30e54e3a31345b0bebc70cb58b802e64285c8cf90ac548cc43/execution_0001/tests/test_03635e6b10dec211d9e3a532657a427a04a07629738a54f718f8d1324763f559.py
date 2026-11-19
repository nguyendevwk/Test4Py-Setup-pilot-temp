import os
import shutil
from pathlib import Path

import pytest

from httpie.config import get_default_config_dir, ENV_HTTPIE_CONFIG_DIR, ENV_XDG_CONFIG_HOME


def test_env_var_overrides_all(monkeypatch, tmp_path):
    """When HTTPIE_CONFIG_DIR is set, that path is returned regardless of other settings."""
    custom_dir = tmp_path / "custom_config"
    custom_dir.mkdir()
    monkeypatch.setenv(ENV_HTTPIE_CONFIG_DIR, str(custom_dir))
    # Ensure other env vars are unset
    monkeypatch.delenv(ENV_XDG_CONFIG_HOME, raising=False)
    # Ensure legacy dir does not exist
    legacy = Path.home() / ".httpie"
    if legacy.exists():
        shutil.rmtree(legacy)
    result = get_default_config_dir()
    assert result == custom_dir
    assert result.is_absolute()


def test_legacy_dir_exists(monkeypatch, tmp_path):
    """If legacy ~/.httpie exists, it is returned even if XDG env is set."""
    legacy_dir = tmp_path / ".httpie"
    legacy_dir.mkdir()
    # Monkeypatch Path.home to point to tmp_path
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    # Set XDG_CONFIG_HOME to a different value
    monkeypatch.setenv(ENV_XDG_CONFIG_HOME, str(tmp_path / "xdg"))
    result = get_default_config_dir()
    assert result == legacy_dir
    assert result.is_absolute()


def test_xdg_default_when_no_legacy(monkeypatch, tmp_path):
    """When no legacy dir and no HTTPIE_CONFIG_DIR, XDG_CONFIG_HOME is used."""
    # Ensure legacy dir does not exist
    legacy_dir = tmp_path / ".httpie"
    if legacy_dir.exists():
        shutil.rmtree(legacy_dir)
    # Set XDG_CONFIG_HOME
    xdg_dir = tmp_path / "xdg"
    xdg_dir.mkdir()
    monkeypatch.setenv(ENV_XDG_CONFIG_HOME, str(xdg_dir))
    # Monkeypatch Path.home to point to tmp_path
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    result = get_default_config_dir()
    expected = xdg_dir / "httpie"
    assert result == expected
    assert result.is_absolute()

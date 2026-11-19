import os
import shutil
from pathlib import Path

import pytest

from httpie.config import get_default_config_dir, ENV_HTTPIE_CONFIG_DIR, ENV_XDG_CONFIG_HOME, DEFAULT_RELATIVE_LEGACY_CONFIG_DIR, DEFAULT_CONFIG_DIRNAME, DEFAULT_WINDOWS_CONFIG_DIR, is_windows


def test_env_override_config_dir(tmp_path, monkeypatch):
    """When ENV_HTTPIE_CONFIG_DIR is set, the function returns that path."""
    custom_dir = tmp_path / "custom_config"
    custom_dir.mkdir()
    monkeypatch.setenv(ENV_HTTPIE_CONFIG_DIR, str(custom_dir))
    result = get_default_config_dir()
    assert result == custom_dir
    # Ensure no other environment variables influence the result
    monkeypatch.delenv(ENV_XDG_CONFIG_HOME, raising=False)
    monkeypatch.delenv(ENV_HTTPIE_CONFIG_DIR, raising=False)


def test_legacy_config_dir_exists(tmp_path, monkeypatch):
    """If the legacy ~/.httpie directory exists, it is returned."""
    # Create a fake home directory
    fake_home = tmp_path / "home"
    fake_home.mkdir()
    # Create the legacy config directory inside it
    legacy_dir = fake_home / DEFAULT_RELATIVE_LEGACY_CONFIG_DIR
    legacy_dir.mkdir()
    # Patch Path.home to return our fake home
    monkeypatch.setattr(Path, "home", lambda: fake_home)
    # Ensure no env override
    monkeypatch.delenv(ENV_HTTPIE_CONFIG_DIR, raising=False)
    result = get_default_config_dir()
    assert result == legacy_dir
    # Clean up
    shutil.rmtree(fake_home)


def test_xdg_default_config_dir(tmp_path, monkeypatch):
    """When no legacy directory and no env override, XDG default is used."""
    # Create a fake home directory without legacy config
    fake_home = tmp_path / "home"
    fake_home.mkdir()
    # Patch Path.home to return our fake home
    monkeypatch.setattr(Path, "home", lambda: fake_home)
    # Ensure no legacy dir
    legacy_dir = fake_home / DEFAULT_RELATIVE_LEGACY_CONFIG_DIR
    assert not legacy_dir.exists()
    # Ensure no env override
    monkeypatch.delenv(ENV_HTTPIE_CONFIG_DIR, raising=False)
    # Ensure no XDG_CONFIG_HOME set
    monkeypatch.delenv(ENV_XDG_CONFIG_HOME, raising=False)
    result = get_default_config_dir()
    expected = fake_home / DEFAULT_RELATIVE_XDG_CONFIG_HOME / DEFAULT_CONFIG_DIRNAME
    assert result == expected

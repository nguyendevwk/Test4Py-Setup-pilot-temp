import json
import os
from pathlib import Path

import pytest

from httpie.config import Config


def test_default_initialization(tmp_path):
    """Config should initialize with default values when no file exists."""
    cfg = Config(directory=tmp_path)
    # default_options should be the default list
    assert cfg.default_options == []
    # plugins_dir should resolve to tmp_path/plugins
    expected_plugins = (tmp_path / "plugins").expanduser().resolve()
    assert cfg.plugins_dir == expected_plugins
    # version_info_file should resolve to tmp_path/version_info.json
    expected_version = (tmp_path / "version_info.json").expanduser().resolve()
    assert cfg.version_info_file == expected_version
    # developer_mode should be None when not set
    assert cfg.developer_mode is None
    # The underlying file should not exist yet
    assert not (tmp_path / Config.FILENAME).exists()


def test_custom_config_file(tmp_path):
    """Config should load values from an existing JSON file."""
    # Create a custom config file with some overrides
    config_path = tmp_path / Config.FILENAME
    data = {
        "default_options": ["--verbose"],
        "plugins_dir": "~/custom_plugins",
        "developer_mode": True
    }
    config_path.write_text(json.dumps(data), encoding="utf-8")

    cfg = Config(directory=tmp_path)

    # default_options should reflect the file
    assert cfg.default_options == ["--verbose"]
    # plugins_dir should expand user and resolve
    expected_plugins = Path("~/custom_plugins").expanduser().resolve()
    assert cfg.plugins_dir == expected_plugins
    # developer_mode should be True
    assert cfg.developer_mode is True
    # version_info_file should still use default
    expected_version = (tmp_path / "version_info.json").expanduser().resolve()
    assert cfg.version_info_file == expected_version


def test_missing_keys_and_updates(tmp_path):
    """Config should handle missing keys gracefully and allow updates."""
    cfg = Config(directory=tmp_path)

    # Accessing a non-existent key via get should return None
    assert cfg.get("nonexistent_key") is None

    # Update a key and verify persistence
    cfg["default_options"] = ["--no-color"]
    assert cfg.default_options == ["--no-color"]

    # Write the config to disk
    cfg.save()  # assuming BaseConfigDict provides a save method

    # Reload from disk and verify values persist
    cfg2 = Config(directory=tmp_path)
    assert cfg2.default_options == ["--no-color"]

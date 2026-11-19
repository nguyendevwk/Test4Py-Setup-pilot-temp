import json
import os
from pathlib import Path

import pytest

from httpie.config import Config, DEFAULT_CONFIG_DIR, get_default_config_dir


def test_default_config_initialization(tmp_path):
    """Config should create a new file with defaults when none exists."""
    cfg_dir = tmp_path / "httpie"
    cfg = Config(directory=cfg_dir)
    # The config file should be created with defaults
    assert cfg.path.exists()
    data = json.loads(cfg.path.read_text(encoding="utf-8"))
    # Default options list is empty
    assert data["default_options"] == []
    # The meta section should contain the current version
    assert "__meta__" in data
    assert "httpie" in data["__meta__"]


def test_custom_config_overrides_and_path_resolution(tmp_path):
    """Custom values in the config file should override defaults and
    path resolution should work for relative and absolute paths."""
    cfg_dir = tmp_path / "httpie"
    cfg_file = cfg_dir / Config.FILENAME
    cfg_dir.mkdir()
    # Write a custom config with relative paths
    custom = {
        "default_options": ["--verbose"],
        "plugins_dir": "my_plugins",
        "version_info_file": "~/my_version.json",
        "developer_mode": True,
    }
    cfg_file.write_text(json.dumps(custom, indent=4), encoding="utf-8")

    cfg = Config(directory=cfg_dir)
    # Load should read the file
    assert cfg["default_options"] == ["--verbose"]
    # Path resolution expands user and resolves to absolute path
    expected_plugins = (cfg_dir / "my_plugins").resolve()
    assert cfg.plugins_dir == expected_plugins
    expected_version_file = Path.home() / "my_version.json"
    assert cfg.version_info_file == expected_version_file.resolve()
    # Developer mode flag is preserved
    assert cfg.developer_mode is True


def test_missing_config_file_uses_default_and_no_error(tmp_path):
    """When the config file is missing, Config should still provide defaults
    and not raise an exception."""
    cfg_dir = tmp_path / "httpie"
    cfg = Config(directory=cfg_dir)
    # No file should exist yet
    assert not cfg.path.exists()
    # Defaults should be present
    assert cfg.default_options == []
    # Plugins dir should resolve to default relative to config dir
    assert cfg.plugins_dir == (cfg_dir / "plugins").resolve()
    # Version info file should resolve to default relative to config dir
    assert cfg.version_info_file == (cfg_dir / "version_info.json").resolve()
    # Developer mode should be None (unset)
    assert cfg.developer_mode is None

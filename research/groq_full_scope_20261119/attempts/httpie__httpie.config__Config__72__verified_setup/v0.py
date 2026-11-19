import json
import os
from pathlib import Path

import pytest

from httpie.config import Config


def test_default_options_and_initialization(tmp_path):
    """Config should initialize with default options and store them in the file."""
    cfg = Config(directory=tmp_path)
    # default_options should be the default list
    assert cfg.default_options == []
    # The config file should exist and contain the defaults
    cfg_file = tmp_path / Config.FILENAME
    assert cfg_file.is_file()
    data = json.loads(cfg_file.read_text(encoding="utf-8"))
    assert data["default_options"] == []


def test_plugins_dir_and_version_info_file_resolution(tmp_path):
    """Config should resolve relative paths correctly and expand user."""
    # Create a custom plugins directory inside tmp_path
    custom_plugins = tmp_path / "my_plugins"
    custom_plugins.mkdir()
    # Create a custom version info file
    custom_version = tmp_path / "my_version.json"
    custom_version.write_text('{"ver":"1.0"}', encoding="utf-8")

    # Write a config file that points to these custom paths
    cfg_file = tmp_path / Config.FILENAME
    cfg_file.write_text(
        json.dumps(
            {
                "plugins_dir": str(custom_plugins),
                "version_info_file": str(custom_version),
            }
        ),
        encoding="utf-8",
    )

    cfg = Config(directory=tmp_path)
    # The resolved paths should match the absolute paths we created
    assert cfg.plugins_dir == custom_plugins.resolve()
    assert cfg.version_info_file == custom_version.resolve()


def test_developer_mode_default_and_override(tmp_path):
    """developer_mode should be None by default and can be overridden."""
    cfg = Config(directory=tmp_path)
    # Default is None (not set)
    assert cfg.developer_mode is None

    # Override the value in the config file
    cfg_file = tmp_path / Config.FILENAME
    cfg_file.write_text(
        json.dumps({"developer_mode": True}), encoding="utf-8"
    )
    # Reinitialize to load the new value
    cfg = Config(directory=tmp_path)
    assert cfg.developer_mode is True

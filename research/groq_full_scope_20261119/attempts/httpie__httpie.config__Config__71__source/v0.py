import json
import os
from pathlib import Path

import pytest

from httpie.config import Config


def test_default_options_and_default_values(tmp_path):
    """Config should contain default options and defaults for missing keys."""
    cfg = Config(directory=tmp_path)
    # default_options should be the default list
    assert cfg.default_options == []
    # plugins_dir should default to tmp_path / 'plugins'
    assert cfg.plugins_dir == tmp_path / "plugins"
    # version_info_file should default to tmp_path / 'version_info.json'
    assert cfg.version_info_file == tmp_path / "version_info.json"
    # developer_mode should be None when not set
    assert cfg.developer_mode is None


def test_custom_plugins_dir_and_user_expansion(tmp_path):
    """Setting a custom plugins_dir should resolve correctly, including ~ expansion."""
    # Create a custom directory under the temp path
    custom_dir = tmp_path / "custom_plugins"
    custom_dir.mkdir()
    # Write a config file with a user path
    config_path = tmp_path / Config.FILENAME
    config_data = {"plugins_dir": f"{custom_dir}"}
    config_path.write_text(json.dumps(config_data))
    cfg = Config(directory=tmp_path)
    # The property should resolve to the absolute path of custom_dir
    assert cfg.plugins_dir == custom_dir.resolve()


def test_missing_config_file_creates_defaults(tmp_path):
    """When no config file exists, Config should still provide defaults."""
    # Ensure no config file exists
    config_path = tmp_path / Config.FILENAME
    if config_path.exists():
        config_path.unlink()
    cfg = Config(directory=tmp_path)
    # The config should still have the default options list
    assert cfg.default_options == []
    # The config file should not be created automatically
    assert not config_path.exists()

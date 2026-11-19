import json
import os
from pathlib import Path

import pytest

from httpie.config import Config, DEFAULT_CONFIG_DIR


def test_default_options_and_directory(tmp_path):
    """Config should load defaults and use the provided directory."""
    # Create a config file with custom default_options
    config_path = tmp_path / "config.json"
    config_data = {"default_options": ["--verbose", "--timeout=30"]}
    config_path.write_text(json.dumps(config_data), encoding="utf-8")

    # Instantiate Config pointing to tmp_path
    cfg = Config(directory=tmp_path)

    # The default_options property should reflect the file content
    assert cfg.default_options == ["--verbose", "--timeout=30"]

    # The directory attribute should be a Path instance pointing to tmp_path
    assert isinstance(cfg.directory, Path)
    assert cfg.directory.resolve() == tmp_path.resolve()


def test_plugins_and_version_info_paths(tmp_path):
    """Config should resolve plugins_dir and version_info_file correctly."""
    # No custom paths in config; should use defaults relative to directory
    cfg = Config(directory=tmp_path)

    # plugins_dir should resolve to <tmp_path>/plugins
    expected_plugins = (tmp_path / "plugins").expanduser().resolve()
    assert cfg.plugins_dir == expected_plugins

    # version_info_file should resolve to <tmp_path>/version_info.json
    expected_version_file = (tmp_path / "version_info.json").expanduser().resolve()
    assert cfg.version_info_file == expected_version_file

    # Now set custom paths in the config file
    custom_data = {
        "plugins_dir": "~/custom_plugins",
        "version_info_file": "/tmp/custom_version.json"
    }
    (tmp_path / "config.json").write_text(json.dumps(custom_data), encoding="utf-8")

    # Reload config
    cfg = Config(directory=tmp_path)

    # plugins_dir should expand ~ and resolve to absolute path
    assert cfg.plugins_dir == Path("~/custom_plugins").expanduser().resolve()

    # version_info_file should be the absolute path as given
    assert cfg.version_info_file == Path("/tmp/custom_version.json").expanduser().resolve()


def test_developer_mode_flag(tmp_path):
    """developer_mode should return the value stored in the config."""
    # Create config with developer_mode set to True
    cfg_data = {"developer_mode": True}
    (tmp_path / "config.json").write_text(json.dumps(cfg_data), encoding="utf-8")

    cfg = Config(directory=tmp_path)
    assert cfg.developer_mode is True

    # If the key is missing, get should return None (falsy)
    (tmp_path / "config.json").write_text(json.dumps({}), encoding="utf-8")
    cfg = Config(directory=tmp_path)
    assert cfg.developer_mode is None

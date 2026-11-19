import json
import os
from pathlib import Path

import pytest

from httpie.config import Config, DEFAULT_CONFIG_DIR


def test_default_options_initialization(tmp_path):
    """Config should contain default_options list after construction."""
    cfg = Config(directory=tmp_path)
    # default_options should be an empty list as per DEFAULTS
    assert isinstance(cfg.default_options, list)
    assert cfg.default_options == []


def test_plugins_dir_path_resolution(tmp_path):
    """plugins_dir should resolve to the configured path or default."""
    cfg = Config(directory=tmp_path)
    # By default, plugins_dir should be <tmp_path>/plugins
    expected_default = (tmp_path / "plugins").expanduser().resolve()
    assert cfg.plugins_dir == expected_default

    # Override the plugins_dir in the config file
    cfg_path = cfg.path
    cfg_path.parent.mkdir(parents=True, exist_ok=True)
    cfg_data = {"plugins_dir": "~/custom_plugins"}
    cfg_path.write_text(json.dumps(cfg_data), encoding="utf-8")
    # Reload the config to pick up the change
    cfg.load()
    expected_custom = Path("~").expanduser().joinpath("custom_plugins").resolve()
    assert cfg.plugins_dir == expected_custom


def test_developer_mode_flag(tmp_path):
    """developer_mode should return the value set in the config file."""
    cfg = Config(directory=tmp_path)
    # Initially, developer_mode is None (falsy)
    assert cfg.developer_mode is None

    # Write a config file with developer_mode set to True
    cfg_path = cfg.path
    cfg_path.parent.mkdir(parents=True, exist_ok=True)
    cfg_data = {"developer_mode": True}
    cfg_path.write_text(json.dumps(cfg_data), encoding="utf-8")
    cfg.load()
    assert cfg.developer_mode is True

    # Write a config file with developer_mode set to False
    cfg_data = {"developer_mode": False}
    cfg_path.write_text(json.dumps(cfg_data), encoding="utf-8")
    cfg.load()
    assert cfg.developer_mode is False

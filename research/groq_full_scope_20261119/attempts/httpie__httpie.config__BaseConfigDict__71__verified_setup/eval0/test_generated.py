import json
import os
from pathlib import Path

import pytest

from httpie.config import BaseConfigDict, __version__


def test_base_config_dict_is_new_and_load_does_nothing(tmp_path: Path):
    """A new config file should be reported as new and loading should not raise."""
    cfg_path = tmp_path / "config.json"
    cfg = BaseConfigDict(cfg_path)
    assert cfg.is_new() is True
    # Loading when file does not exist should not raise and should leave dict empty
    cfg.load()
    assert cfg == {}


def test_base_config_dict_save_and_meta(tmp_path: Path):
    """Saving a config should create the file and include meta information."""
    cfg_path = tmp_path / "config.json"
    cfg = BaseConfigDict(cfg_path)
    cfg["foo"] = "bar"
    # Set helpurl and about to test meta inclusion
    cfg.helpurl = "https://example.com/help"
    cfg.about = "Test config"
    cfg.save(bump_version=True)

    # File should exist and contain JSON
    assert cfg_path.exists()
    content = cfg_path.read_text(encoding="utf-8")
    data = json.loads(content)

    # Check that user data is present
    assert data["foo"] == "bar"
    # Meta should contain httpie version, help, and about
    meta = data.get("__meta__", {})
    assert meta["httpie"] == __version__
    assert meta["help"] == "https://example.com/help"
    assert meta["about"] == "Test config"


def test_base_config_dict_load_persists_data(tmp_path: Path):
    """Data written by one instance should be loadable by another instance."""
    cfg_path = tmp_path / "config.json"
    cfg1 = BaseConfigDict(cfg_path)
    cfg1["alpha"] = 1
    cfg1["beta"] = 2
    cfg1.save()

    cfg2 = BaseConfigDict(cfg_path)
    cfg2.load()
    # The loaded data should match what was saved
    assert cfg2["alpha"] == 1
    assert cfg2["beta"] == 2
    # Ensure that meta defaults to current version if not present
    assert cfg2.version == __version__

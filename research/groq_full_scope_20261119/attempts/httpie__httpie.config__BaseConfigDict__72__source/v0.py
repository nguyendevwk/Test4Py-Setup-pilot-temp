import json
import os
from pathlib import Path

import pytest

from httpie.config import BaseConfigDict
from httpie import __version__


def test_save_and_load_roundtrip(tmp_path: Path):
    """Test that a config can be saved and then loaded back with the same data."""
    cfg_path = tmp_path / "config.json"
    cfg = BaseConfigDict(cfg_path)
    cfg.update({"foo": "bar", "number": 42})
    cfg.helpurl = "https://example.com/help"
    cfg.about = "Test config"
    cfg.save(bump_version=True)

    # Ensure file exists and contains JSON
    assert cfg_path.exists()
    raw = cfg_path.read_text(encoding="utf-8")
    data = json.loads(raw)
    assert data["foo"] == "bar"
    assert data["number"] == 42
    assert data["__meta__"]["httpie"] == __version__
    assert data["__meta__"]["help"] == "https://example.com/help"
    assert data["__meta__"]["about"] == "Test config"

    # Load into a new instance
    new_cfg = BaseConfigDict(cfg_path)
    new_cfg.load()
    assert new_cfg["foo"] == "bar"
    assert new_cfg["number"] == 42
    assert new_cfg["__meta__"]["httpie"] == __version__
    assert new_cfg["__meta__"]["help"] == "https://example.com/help"
    assert new_cfg["__meta__"]["about"] == "Test config"


def test_is_new_and_ensure_directory(tmp_path: Path):
    """Test that is_new reports correctly and ensure_directory creates the folder."""
    cfg_path = tmp_path / "subdir" / "config.json"
    cfg = BaseConfigDict(cfg_path)

    # Before creation, path does not exist
    assert cfg.is_new() is True
    assert not cfg_path.parent.exists()

    # ensure_directory should create the parent directory
    cfg.ensure_directory()
    assert cfg_path.parent.exists()
    assert cfg_path.parent.is_dir()

    # After creation, is_new should be False
    assert cfg.is_new() is False


def test_pre_and_post_process_hooks(tmp_path: Path):
    """Test that pre_process_data and post_process_data hooks are called."""
    class HookedConfig(BaseConfigDict):
        def pre_process_data(self, data):
            # Convert all string values to uppercase during load
            return {k: v.upper() if isinstance(v, str) else v for k, v in data.items()}

        def post_process_data(self, data):
            # Add a marker during save
            data = dict(data)  # copy to avoid mutating original
            data["__meta__"]["saved"] = True
            return data

    cfg_path = tmp_path / "hook.json"
    cfg = HookedConfig(cfg_path)
    cfg.update({"msg": "hello", "count": 3})
    cfg.save()

    # Load into a new instance and check pre_process_data effect
    new_cfg = HookedConfig(cfg_path)
    new_cfg.load()
    assert new_cfg["msg"] == "HELLO"
    assert new_cfg["count"] == 3

    # Verify that post_process_data added the marker
    raw = cfg_path.read_text(encoding="utf-8")
    data = json.loads(raw)
    assert data["__meta__"]["saved"] is True

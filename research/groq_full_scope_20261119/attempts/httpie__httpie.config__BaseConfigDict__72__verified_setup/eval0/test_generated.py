import json
import os
import sys
import tempfile
from pathlib import Path

import pytest

# Import the target class from the installed package
from httpie.config import BaseConfigDict


def test_base_config_dict_is_new_and_save(tmp_path: Path):
    """
    Verify that a new BaseConfigDict reports itself as new,
    can be saved to disk, and that the file contains the expected JSON.
    """
    cfg_path = tmp_path / "config.json"
    cfg = BaseConfigDict(cfg_path)

    # Initially the file does not exist
    assert cfg.is_new() is True

    # Set some data and save
    cfg["foo"] = "bar"
    cfg.save(bump_version=True)

    # After saving, the file should exist and the config should not be new
    assert cfg_path.exists()
    assert cfg.is_new() is False

    # Load the file content and compare with the expected JSON
    with cfg_path.open("r", encoding="utf-8") as f:
        content = json.load(f)
    # The saved JSON should contain the key we set
    assert content["foo"] == "bar"
    # The meta section should contain the httpie version
    assert "__meta__" in content
    assert "httpie" in content["__meta__"]


def test_base_config_dict_load_and_pre_post_processing(tmp_path: Path):
    """
    Verify that load correctly reads a JSON file and that
    pre_process_data and post_process_data hooks are respected.
    """
    cfg_path = tmp_path / "config.json"

    # Create a JSON file with a custom key
    original_data = {"custom": "value", "__meta__": {"httpie": "1.0.0"}}
    cfg_path.write_text(json.dumps(original_data, indent=4), encoding="utf-8")

    # Subclass BaseConfigDict to override hooks
    class HookedConfigDict(BaseConfigDict):
        def pre_process_data(self, data):
            # Remove the custom key before loading
            data.pop("custom", None)
            return data

        def post_process_data(self, data):
            # Add a new key before saving
            data["added"] = "yes"
            return data

    cfg = HookedConfigDict(cfg_path)
    cfg.load()

    # The custom key should have been removed by pre_process_data
    assert "custom" not in cfg
    # The meta httpie version should be preserved
    assert cfg["__meta__"]["httpie"] == "1.0.0"

    # Save the config and verify that the post_process_data added the key
    cfg.save()
    with cfg_path.open("r", encoding="utf-8") as f:
        saved = json.load(f)
    assert "added" in saved
    assert saved["added"] == "yes"


def test_base_config_dict_version_property(tmp_path: Path):
    """
    Verify that the version property returns the stored httpie version
    or falls back to the package __version__ if not present.
    """
    cfg_path = tmp_path / "config.json"

    # Create a config without a __meta__ section
    cfg_path.write_text("{}", encoding="utf-8")

    cfg = BaseConfigDict(cfg_path)
    cfg.load()

    # Since no meta section, version should be the package's __version__
    from httpie import __version__ as pkg_version
    assert cfg.version == pkg_version

    # Now add a meta section with a different version
    cfg["__meta__"] = {"httpie": "9.9.9"}
    assert cfg.version == "9.9.9"

import json
import os
import pytest
from pathlib import Path
from httpie.config import BaseConfigDict, __version__

# Helper subclass to expose hooks for testing
class TestConfig(BaseConfigDict):
    name = "testconfig"
    helpurl = "https://example.com/help"
    about = "Test configuration"

    def pre_process_data(self, data):
        # Add a marker to verify pre-processing
        data["pre_processed"] = True
        return data

    def post_process_data(self, data):
        # Add a marker to verify post-processing
        data["post_processed"] = True
        return data

@pytest.fixture
def config_path(tmp_path):
    return tmp_path / "config.json"

def test_save_creates_file_and_includes_meta_and_hooks(config_path):
    cfg = TestConfig(config_path)
    cfg["key"] = "value"
    cfg.save(bump_version=True)

    # File should exist
    assert config_path.exists()
    # Load raw JSON to verify contents
    raw = json.loads(config_path.read_text(encoding="utf-8"))
    # Meta should contain httpie version and help/about
    assert "__meta__" in raw
    assert raw["__meta__"]["httpie"] == __version__
    assert raw["__meta__"]["help"] == cfg.helpurl
    assert raw["__meta__"]["about"] == cfg.about
    # Post-processing marker should be present
    assert raw["post_processed"] is True
    # Original key should be preserved
    assert raw["key"] == "value"

def test_load_reads_and_preprocesses(config_path):
    # Prepare a config file with some data
    initial = {"foo": "bar", "pre_processed": False}
    config_path.write_text(json.dumps(initial, indent=4, sort_keys=True), encoding="utf-8")
    cfg = TestConfig(config_path)
    cfg.load()
    # After load, pre_process_data should have set the marker
    assert cfg["pre_processed"] is True
    # Existing data should be present
    assert cfg["foo"] == "bar"

def test_is_new_and_save_when_file_missing(tmp_path):
    missing_path = tmp_path / "missing.json"
    cfg = TestConfig(missing_path)
    # File does not exist yet
    assert cfg.is_new() is True
    cfg["x"] = 1
    cfg.save()
    # After saving, file should exist and is_new should be False
    assert missing_path.exists()
    assert cfg.is_new() is False
    # Verify that the file contains the key
    loaded = json.loads(missing_path.read_text(encoding="utf-8"))
    assert loaded["x"] == 1

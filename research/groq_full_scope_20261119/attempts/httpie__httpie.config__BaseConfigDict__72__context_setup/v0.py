import json
import os
import pytest
from pathlib import Path
from httpie.config import BaseConfigDict, read_raw_config, ConfigFileError, __version__

class TestBaseConfigDict:
    def test_save_and_load_roundtrip(self, tmp_path):
        """Verify that a config can be saved and loaded correctly."""
        cfg_path = tmp_path / "config.json"
        cfg = BaseConfigDict(cfg_path)
        cfg.update({"foo": "bar", "number": 42})
        cfg.helpurl = "https://example.com"
        cfg.about = "Test config"
        cfg.save(bump_version=True)

        # The file should exist and contain JSON
        assert cfg_path.exists()
        with cfg_path.open(encoding="utf-8") as f:
            data = json.load(f)
        # Meta information must be present
        assert "__meta__" in data
        assert data["__meta__"]["httpie"] == __version__
        assert data["__meta__"]["help"] == "https://example.com"
        assert data["__meta__"]["about"] == "Test config"
        # Original keys preserved
        assert data["foo"] == "bar"
        assert data["number"] == 42

        # Load into a new instance
        new_cfg = BaseConfigDict(cfg_path)
        new_cfg.load()
        assert new_cfg["foo"] == "bar"
        assert new_cfg["number"] == 42
        assert new_cfg["__meta__"]["httpie"] == __version__

    def test_is_new_and_directory_creation(self, tmp_path):
        """Ensure that a new config reports as new and creates its directory."""
        subdir = tmp_path / "nested" / "dir"
        cfg_path = subdir / "config.json"
        cfg = BaseConfigDict(cfg_path)
        # Before any file exists, is_new should be True
        assert cfg.is_new()
        # After saving, the directory should be created
        cfg.update({"key": "value"})
        cfg.save()
        assert cfg_path.exists()
        assert subdir.exists()
        # Now is_new should be False
        assert not cfg.is_new()

    def test_load_invalid_json_raises(self, tmp_path):
        """Loading a file with malformed JSON should raise ConfigFileError."""
        cfg_path = tmp_path / "bad.json"
        # Write invalid JSON
        cfg_path.write_text("{invalid json}", encoding="utf-8")
        # Attempt to load should raise
        with pytest.raises(ConfigFileError) as excinfo:
            read_raw_config("baseconfigdict", cfg_path)
        assert "invalid baseconfigdict file" in str(excinfo.value)

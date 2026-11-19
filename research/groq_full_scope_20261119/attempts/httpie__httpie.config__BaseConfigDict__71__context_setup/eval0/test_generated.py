import json
import os
import pytest
from pathlib import Path
from httpie.config import BaseConfigDict, read_raw_config, ConfigFileError, __version__

class DummyConfig(BaseConfigDict):
    name = "dummy"
    helpurl = "https://example.com"
    about = "Test config"

def test_save_and_load_roundtrip(tmp_path: Path):
    cfg_path = tmp_path / "dummy.json"
    cfg = DummyConfig(cfg_path)
    cfg["key"] = "value"
    cfg.save(bump_version=True)

    # Ensure file exists and contains expected JSON
    assert cfg_path.exists()
    content = cfg_path.read_text(encoding="utf-8")
    data = json.loads(content)
    assert data["key"] == "value"
    assert data["__meta__"]["httpie"] == __version__
    assert data["__meta__"]["help"] == DummyConfig.helpurl
    assert data["__meta__"]["about"] == DummyConfig.about

    # Load into a new instance and verify data
    new_cfg = DummyConfig(cfg_path)
    new_cfg.load()
    assert new_cfg["key"] == "value"
    assert new_cfg.version == __version__

def test_load_with_missing_file(tmp_path: Path):
    cfg_path = tmp_path / "missing.json"
    cfg = DummyConfig(cfg_path)
    # Loading should not raise and should leave dict empty
    cfg.load()
    assert cfg == {}
    # After saving, file should be created
    cfg["foo"] = "bar"
    cfg.save()
    assert cfg_path.exists()
    loaded_cfg = DummyConfig(cfg_path)
    loaded_cfg.load()
    assert loaded_cfg["foo"] == "bar"

def test_load_invalid_json(tmp_path: Path):
    cfg_path = tmp_path / "invalid.json"
    cfg_path.write_text("not a json", encoding="utf-8")
    with pytest.raises(ConfigFileError) as excinfo:
        read_raw_config("dummy", cfg_path)
    assert "invalid dummy file" in str(excinfo.value)

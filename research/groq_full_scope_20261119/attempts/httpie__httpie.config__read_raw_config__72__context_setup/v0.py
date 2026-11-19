import json
import os
import pytest
from pathlib import Path
from httpie.config import read_raw_config, ConfigFileError

def test_read_raw_config_success(tmp_path: Path):
    # Create a valid JSON config file
    config_path = tmp_path / "config.json"
    data = {"key": "value", "number": 42}
    config_path.write_text(json.dumps(data), encoding="utf-8")

    # Read the config and verify the returned dictionary matches the file contents
    result = read_raw_config("test", config_path)
    assert isinstance(result, dict)
    assert result == data
    assert result["key"] == "value"
    assert result["number"] == 42

def test_read_raw_config_file_not_found(tmp_path: Path):
    # Path to a non-existent file
    missing_path = tmp_path / "missing.json"

    # read_raw_config should return None when the file does not exist
    result = read_raw_config("test", missing_path)
    assert result is None

def test_read_raw_config_invalid_json(tmp_path: Path):
    # Create a file with invalid JSON content
    bad_path = tmp_path / "bad.json"
    bad_path.write_text("{invalid json}", encoding="utf-8")

    # Attempting to read should raise ConfigFileError with a message containing the file path
    with pytest.raises(ConfigFileError) as excinfo:
        read_raw_config("test", bad_path)
    error_msg = str(excinfo.value)
    assert "invalid test file" in error_msg
    assert str(bad_path) in error_msg
    assert "invalid JSON" in error_msg or "Expecting" in error_msg

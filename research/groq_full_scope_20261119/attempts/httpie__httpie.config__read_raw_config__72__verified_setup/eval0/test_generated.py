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

    # Read the config using the function
    result = read_raw_config("test", config_path)

    # Assert that the returned dictionary matches the original data
    assert isinstance(result, dict)
    assert result == data
    assert result["key"] == "value"
    assert result["number"] == 42

def test_read_raw_config_invalid_json(tmp_path: Path):
    # Create a file with invalid JSON content
    bad_path = tmp_path / "bad.json"
    bad_path.write_text("{invalid json}", encoding="utf-8")

    # Expect ConfigFileError to be raised with a message containing the file path
    with pytest.raises(ConfigFileError) as excinfo:
        read_raw_config("test", bad_path)

    # Verify that the exception message references the file path
    assert str(bad_path) in str(excinfo.value)
    assert "invalid test file" in str(excinfo.value)

def test_read_raw_config_missing_file(tmp_path: Path):
    # Define a path that does not exist
    missing_path = tmp_path / "does_not_exist.json"

    # The function should return an empty dict when the file is missing
    result = read_raw_config("test", missing_path)

    # Assert that the result is an empty dictionary
    assert result == {}
    assert isinstance(result, dict)

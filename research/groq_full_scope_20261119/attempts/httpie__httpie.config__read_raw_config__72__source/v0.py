import json
import os
from pathlib import Path

import pytest

from httpie.config import read_raw_config, ConfigFileError


def test_read_raw_config_valid(tmp_path: Path):
    """Reading a valid JSON configuration returns the expected dictionary."""
    config_data = {"key": "value", "number": 42}
    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps(config_data), encoding="utf-8")

    result = read_raw_config("test", config_file)
    assert isinstance(result, dict)
    assert result == config_data
    assert result["key"] == "value"
    assert result["number"] == 42


def test_read_raw_config_invalid_json(tmp_path: Path):
    """An invalid JSON file raises ConfigFileError with a helpful message."""
    bad_file = tmp_path / "bad.json"
    bad_file.write_text("{invalid json}", encoding="utf-8")

    with pytest.raises(ConfigFileError) as excinfo:
        read_raw_config("test", bad_file)

    err_msg = str(excinfo.value)
    assert "invalid test file" in err_msg
    assert "bad.json" in err_msg
    assert "invalid" in err_msg  # part of the ValueError message


def test_read_raw_config_missing_file(tmp_path: Path):
    """If the configuration file does not exist, read_raw_config returns an empty dict."""
    missing_file = tmp_path / "does_not_exist.json"

    result = read_raw_config("test", missing_file)
    assert result == {}

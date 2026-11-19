import json
import os
from pathlib import Path

import pytest

from httpie.config import read_raw_config, ConfigFileError


def test_read_raw_config_valid_json(tmp_path: Path):
    """Reading a valid JSON config file returns the parsed dictionary."""
    config_path = tmp_path / "config.json"
    data = {"key": "value", "number": 42}
    config_path.write_text(json.dumps(data), encoding="utf-8")

    result = read_raw_config("test", config_path)

    assert isinstance(result, dict)
    assert result == data
    assert result is not data  # ensure a new dict was created


def test_read_raw_config_invalid_json(tmp_path: Path):
    """An invalid JSON file raises ConfigFileError with a helpful message."""
    config_path = tmp_path / "bad.json"
    config_path.write_text("{invalid json", encoding="utf-8")

    with pytest.raises(ConfigFileError) as excinfo:
        read_raw_config("test", config_path)

    err_msg = str(excinfo.value)
    assert "invalid test file" in err_msg
    assert str(config_path) in err_msg
    assert "Expecting" in err_msg or "unterminated" in err_msg  # json error text


def test_read_raw_config_missing_file(tmp_path: Path):
    """If the config file does not exist, read_raw_config returns an empty dict."""
    missing_path = tmp_path / "does_not_exist.json"

    result = read_raw_config("test", missing_path)

    assert result == {}
    assert isinstance(result, dict)

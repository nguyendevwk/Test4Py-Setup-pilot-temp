import json
import os
import pytest
from pathlib import Path
from cookiecutter.replay import load, get_file_name

def test_load_success(tmp_path: Path):
    """Verify that load returns the expected dictionary when the JSON file contains a cookiecutter key."""
    # Arrange
    replay_dir = tmp_path / "replay"
    replay_dir.mkdir()
    template_name = "my_template"
    replay_file = get_file_name(replay_dir, template_name)
    data = {"cookiecutter": {"name": "test"}, "other": 123}
    replay_file.write_text(json.dumps(data), encoding="utf-8")

    # Act
    result = load(replay_dir, template_name)

    # Assert
    assert isinstance(result, dict)
    assert result == data
    assert "cookiecutter" in result
    assert result["cookiecutter"]["name"] == "test"

def test_load_missing_cookiecutter_key(tmp_path: Path):
    """Verify that load raises ValueError when the JSON file lacks a cookiecutter key."""
    # Arrange
    replay_dir = tmp_path / "replay"
    replay_dir.mkdir()
    template_name = "missing_key"
    replay_file = get_file_name(replay_dir, template_name)
    data = {"not_cookiecutter": {"foo": "bar"}}
    replay_file.write_text(json.dumps(data), encoding="utf-8")

    # Act & Assert
    with pytest.raises(ValueError, match="Context is required to contain a cookiecutter key"):
        load(replay_dir, template_name)

def test_load_invalid_json(tmp_path: Path):
    """Verify that load propagates JSONDecodeError when the file contains invalid JSON."""
    # Arrange
    replay_dir = tmp_path / "replay"
    replay_dir.mkdir()
    template_name = "invalid_json"
    replay_file = get_file_name(replay_dir, template_name)
    # Write malformed JSON
    replay_file.write_text("{invalid json}", encoding="utf-8")

    # Act & Assert
    with pytest.raises(json.JSONDecodeError):
        load(replay_dir, template_name)

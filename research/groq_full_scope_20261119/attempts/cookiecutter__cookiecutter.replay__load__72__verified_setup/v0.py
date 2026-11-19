import json
import os
import pytest
from pathlib import Path
from cookiecutter.replay import load

def test_load_success(tmp_path: Path):
    """Verify that a valid replay file is loaded correctly."""
    # Arrange: create a replay file with a cookiecutter key
    replay_dir = tmp_path / "replay"
    replay_dir.mkdir()
    replay_file = replay_dir / "my_template.json"
    data = {"cookiecutter": {"name": "example"}, "other": 123}
    replay_file.write_text(json.dumps(data), encoding="utf-8")

    # Act: load the file
    result = load(replay_dir, "my_template")

    # Assert: the returned dict matches the file content
    assert result == data
    assert "cookiecutter" in result
    assert result["cookiecutter"]["name"] == "example"

def test_load_missing_cookiecutter(tmp_path: Path):
    """Ensure a ValueError is raised when the cookiecutter key is absent."""
    # Arrange: create a replay file without the required key
    replay_dir = tmp_path / "replay"
    replay_dir.mkdir()
    replay_file = replay_dir / "missing_key.json"
    data = {"not_cookiecutter": {"name": "example"}}
    replay_file.write_text(json.dumps(data), encoding="utf-8")

    # Act & Assert: loading should raise ValueError
    with pytest.raises(ValueError) as excinfo:
        load(replay_dir, "missing_key")
    assert "Context is required to contain a cookiecutter key" in str(excinfo.value)

def test_load_invalid_json(tmp_path: Path):
    """Verify that a JSONDecodeError is raised for malformed JSON."""
    # Arrange: create a replay file with invalid JSON
    replay_dir = tmp_path / "replay"
    replay_dir.mkdir()
    replay_file = replay_dir / "bad.json"
    replay_file.write_text("{invalid json}", encoding="utf-8")

    # Act & Assert: loading should raise JSONDecodeError
    with pytest.raises(json.JSONDecodeError):
        load(replay_dir, "bad")

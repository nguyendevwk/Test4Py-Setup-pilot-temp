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

    # Assert: the returned dict matches the file contents
    assert result == data
    assert "cookiecutter" in result
    assert result["cookiecutter"]["name"] == "example"

def test_load_missing_cookiecutter(tmp_path: Path):
    """Loading a file without a cookiecutter key should raise ValueError."""
    # Arrange: create a replay file missing the required key
    replay_dir = tmp_path / "replay"
    replay_dir.mkdir()
    replay_file = replay_dir / "bad_template.json"
    data = {"not_cookiecutter": {"name": "example"}}
    replay_file.write_text(json.dumps(data), encoding="utf-8")

    # Act & Assert: expect ValueError with specific message
    with pytest.raises(ValueError, match="Context is required to contain a cookiecutter key"):
        load(replay_dir, "bad_template")

def test_load_invalid_json(tmp_path: Path):
    """Loading a file with malformed JSON should raise JSONDecodeError."""
    # Arrange: create a replay file with invalid JSON
    replay_dir = tmp_path / "replay"
    replay_dir.mkdir()
    replay_file = replay_dir / "invalid.json"
    replay_file.write_text("{invalid json}", encoding="utf-8")

    # Act & Assert: expect json.JSONDecodeError
    with pytest.raises(json.JSONDecodeError):
        load(replay_dir, "invalid")

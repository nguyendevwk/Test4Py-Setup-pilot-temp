import json
import os
import pytest
from pathlib import Path

from cookiecutter.replay import load, get_file_name


def test_load_success(tmp_path: Path):
    """Normal case: JSON file contains a cookiecutter key."""
    data = {"cookiecutter": {"name": "example"}, "other": 123}
    file_path = tmp_path / "replay.json"
    file_path.write_text(json.dumps(data), encoding="utf-8")

    result = load(tmp_path, "replay.json")
    assert result == data
    assert "cookiecutter" in result
    assert result["cookiecutter"]["name"] == "example"


def test_load_missing_cookiecutter(tmp_path: Path):
    """Error case: JSON file lacks the required 'cookiecutter' key."""
    data = {"not_cookiecutter": {"name": "example"}}
    file_path = tmp_path / "replay.json"
    file_path.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(ValueError, match="Context is required to contain a cookiecutter key"):
        load(tmp_path, "replay.json")


def test_get_file_name_with_suffix(tmp_path: Path):
    """Boundary case: template_name already ends with .json, no extra suffix added."""
    replay_dir = tmp_path
    template_name = "template.json"
    expected = os.path.join(replay_dir, "template.json")
    result = get_file_name(replay_dir, template_name)
    assert result == expected

import json
import os
import pytest
from pathlib import Path

from cookiecutter.replay import dump, get_file_name


def test_dump_writes_json_file(tmp_path: Path):
    """Normal case: dump writes a JSON file with the given context."""
    replay_dir = tmp_path / "replay"
    template_name = "my_template"
    context = {"cookiecutter": {"name": "test"}, "other": 123}

    dump(replay_dir, template_name, context)

    expected_file = replay_dir / f"{template_name}.json"
    assert expected_file.exists(), f"Expected file {expected_file} to exist"

    with expected_file.open("r", encoding="utf-8") as f:
        data = json.load(f)
    assert data == context, "File contents do not match the context"


def test_get_file_name_avoids_double_suffix():
    """Boundary case: template name already ending with .json should not get another suffix."""
    replay_dir = "/tmp"
    template_name = "already.json"
    result = get_file_name(replay_dir, template_name)
    expected = os.path.join(replay_dir, "already.json")
    assert result == expected, f"Expected {expected}, got {result}"


def test_dump_raises_value_error_when_cookiecutter_missing(tmp_path: Path):
    """Error case: dump should raise ValueError if 'cookiecutter' key is missing."""
    replay_dir = tmp_path / "replay"
    template_name = "template"
    context = {"not_cookiecutter": True}

    with pytest.raises(ValueError, match="Context is required to contain a cookiecutter key"):
        dump(replay_dir, template_name, context)

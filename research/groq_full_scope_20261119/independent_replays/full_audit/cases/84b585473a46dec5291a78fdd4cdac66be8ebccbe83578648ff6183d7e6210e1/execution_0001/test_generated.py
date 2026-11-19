import json
import os
import pytest
from pathlib import Path

from cookiecutter.replay import dump, get_file_name


def test_dump_creates_json_file(tmp_path):
    """Normal case: dump writes a JSON file with the given context."""
    replay_dir = tmp_path / "replay"
    template_name = "my_template"
    context = {"cookiecutter": {"name": "Alice"}, "other": 123}

    dump(replay_dir, template_name, context)

    expected_file = replay_dir / f"{template_name}.json"
    assert expected_file.exists(), "Expected JSON file was not created"

    with expected_file.open("r", encoding="utf-8") as f:
        data = json.load(f)
    assert data == context, "File contents do not match the context"


def test_get_file_name_no_suffix(tmp_path):
    """Boundary case: template name already ends with .json, no duplicate suffix."""
    replay_dir = tmp_path
    template_name = "existing.json"
    expected_path = os.path.join(replay_dir, template_name)

    result = get_file_name(replay_dir, template_name)
    assert result == expected_path, "File name should not add an extra .json suffix"


def test_dump_missing_cookiecutter_raises(tmp_path):
    """Error case: context without 'cookiecutter' key raises ValueError."""
    replay_dir = tmp_path
    template_name = "template"
    context = {"foo": "bar"}

    with pytest.raises(ValueError) as excinfo:
        dump(replay_dir, template_name, context)

    assert "Context is required to contain a cookiecutter key" in str(excinfo.value)

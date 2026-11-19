import json
import os
from pathlib import Path

import pytest

from cookiecutter.replay import dump, get_file_name


def test_dump_creates_file_and_writes_json(tmp_path: Path) -> None:
    """Normal case: dump writes JSON to the expected file."""
    replay_dir = tmp_path / "replay"
    template_name = "my_template"
    context = {"cookiecutter": {"name": "Alice"}, "other": 123}

    dump(replay_dir, template_name, context)

    # Directory should exist
    assert replay_dir.is_dir()

    # File should exist
    replay_file = get_file_name(replay_dir, template_name)
    assert replay_file.is_file()

    # File content should match the context
    with replay_file.open("r", encoding="utf-8") as f:
        data = json.load(f)
    assert data == context


def test_dump_raises_value_error_when_cookiecutter_missing(tmp_path: Path) -> None:
    """Error case: missing 'cookiecutter' key in context raises ValueError."""
    replay_dir = tmp_path / "replay"
    template_name = "my_template"
    context = {"other": 123}

    with pytest.raises(ValueError, match="Context is required to contain a cookiecutter key"):
        dump(replay_dir, template_name, context)


def test_dump_overwrites_existing_file(tmp_path: Path) -> None:
    """Boundary case: calling dump twice overwrites the previous file."""
    replay_dir = tmp_path / "replay"
    template_name = "my_template"
    first_context = {"cookiecutter": {"name": "Alice"}, "other": 123}
    second_context = {"cookiecutter": {"name": "Bob"}, "other": 456}

    dump(replay_dir, template_name, first_context)
    first_file = get_file_name(replay_dir, template_name)
    assert first_file.read_text(encoding="utf-8") == json.dumps(first_context, indent=2)

    dump(replay_dir, template_name, second_context)
    second_file = get_file_name(replay_dir, template_name)
    assert second_file.read_text(encoding="utf-8") == json.dumps(second_context, indent=2)
    # Ensure the file was overwritten, not duplicated
    assert first_file.read_text(encoding="utf-8") == json.dumps(second_context, indent=2)

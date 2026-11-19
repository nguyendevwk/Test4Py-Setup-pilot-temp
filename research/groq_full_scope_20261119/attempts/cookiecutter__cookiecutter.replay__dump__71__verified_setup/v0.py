import json
import os
import pytest
from pathlib import Path
from cookiecutter.replay import dump

def test_dump_writes_valid_context(tmp_path: Path):
    """Normal case: dump writes JSON with proper indentation."""
    replay_dir = tmp_path / "replay"
    template_name = "my_template"
    context = {"cookiecutter": {"name": "test"}, "other": 123}

    dump(replay_dir, template_name, context)

    expected_file = replay_dir / f"{template_name}.json"
    assert expected_file.exists(), "Replay file should be created"

    with expected_file.open("r", encoding="utf-8") as f:
        data = json.load(f)

    assert data == context, "File contents must match the context"
    # Check indentation by reading raw text
    raw = expected_file.read_text(encoding="utf-8")
    assert raw.count("\n") > 1, "Output should be pretty‑printed with multiple lines"

def test_dump_creates_directory(tmp_path: Path):
    """Boundary case: ensure the replay directory is created if missing."""
    replay_dir = tmp_path / "nonexistent" / "subdir"
    template_name = "template"
    context = {"cookiecutter": {"foo": "bar"}}

    dump(replay_dir, template_name, context)

    assert replay_dir.is_dir(), "dump should create missing directories"
    assert (replay_dir / f"{template_name}.json").exists(), "File should be created in new directory"

def test_dump_raises_on_missing_cookiecutter(tmp_path: Path):
    """Error case: ValueError is raised when 'cookiecutter' key is absent."""
    replay_dir = tmp_path / "replay"
    template_name = "template"
    context = {"not_cookiecutter": {"x": 1}}

    with pytest.raises(ValueError) as excinfo:
        dump(replay_dir, template_name, context)

    assert "cookiecutter" in str(excinfo.value), "Error message should mention missing key"
    # Ensure no file was created
    assert not (replay_dir / f"{template_name}.json").exists(), "No file should be written on error"

import json
import os
import pytest
from pathlib import Path
from cookiecutter.replay import dump

def test_dump_writes_valid_context(tmp_path: Path):
    """Normal case: context contains 'cookiecutter' key and is written to file."""
    replay_dir = tmp_path / "replay"
    template_name = "my_template"
    context = {"cookiecutter": {"name": "test"}, "extra": 123}
    dump(replay_dir, template_name, context)

    # Verify file exists
    replay_file = replay_dir / f"{template_name}.json"
    assert replay_file.exists(), "Replay file was not created"

    # Verify content matches the context
    with replay_file.open("r", encoding="utf-8") as f:
        data = json.load(f)
    assert data == context, "Dumped JSON does not match the original context"

def test_dump_creates_missing_directory(tmp_path: Path):
    """Boundary case: replay directory does not exist before calling dump."""
    replay_dir = tmp_path / "nonexistent" / "subdir"
    template_name = "boundary_test"
    context = {"cookiecutter": {"value": "boundary"}}

    # Ensure directory does not exist initially
    assert not replay_dir.exists()

    dump(replay_dir, template_name, context)

    # Directory should now exist
    assert replay_dir.exists() and replay_dir.is_dir(), "Replay directory was not created"

    # Verify file content
    replay_file = replay_dir / f"{template_name}.json"
    with replay_file.open("r", encoding="utf-8") as f:
        data = json.load(f)
    assert data == context, "Dumped JSON does not match the original context"

def test_dump_raises_value_error_on_missing_cookiecutter(tmp_path: Path):
    """Error case: context missing the required 'cookiecutter' key."""
    replay_dir = tmp_path / "error"
    template_name = "error_test"
    context = {"not_cookiecutter": {"foo": "bar"}}

    with pytest.raises(ValueError) as excinfo:
        dump(replay_dir, template_name, context)

    assert "Context is required to contain a cookiecutter key" in str(excinfo.value)
    # Ensure no file was created
    replay_file = replay_dir / f"{template_name}.json"
    assert not replay_file.exists(), "File should not be created when context is invalid"

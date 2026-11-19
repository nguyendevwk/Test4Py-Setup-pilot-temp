import os
import pytest
from cookiecutter.replay import get_file_name
from pathlib import Path

def test_get_file_name_appends_suffix(tmp_path: Path):
    """When template_name has no .json suffix, the function appends it."""
    replay_dir = tmp_path
    template_name = "my_template"
    expected = os.path.join(str(replay_dir), "my_template.json")
    result = get_file_name(replay_dir, template_name)
    assert result == expected

def test_get_file_name_no_suffix_needed(tmp_path: Path):
    """When template_name already ends with .json, no extra suffix is added."""
    replay_dir = tmp_path
    template_name = "existing.json"
    expected = os.path.join(str(replay_dir), "existing.json")
    result = get_file_name(replay_dir, template_name)
    assert result == expected

def test_get_file_name_invalid_replay_dir_raises():
    """Providing a non‑pathlike replay_dir should raise a TypeError."""
    replay_dir = None  # not a string or Path
    template_name = "template"
    with pytest.raises(TypeError):
        get_file_name(replay_dir, template_name)

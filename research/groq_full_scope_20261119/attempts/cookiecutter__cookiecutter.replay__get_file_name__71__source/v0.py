import os
import pytest
from pathlib import Path
from cookiecutter.replay import get_file_name

def test_get_file_name_adds_suffix(tmp_path: Path):
    """When template_name does not end with .json, a suffix is added."""
    replay_dir = tmp_path
    template_name = "my_template"
    expected = os.path.join(str(replay_dir), "my_template.json")
    result = get_file_name(replay_dir, template_name)
    assert result == expected, f"Expected {expected!r}, got {result!r}"

def test_get_file_name_no_suffix(tmp_path: Path):
    """When template_name already ends with .json, no extra suffix is added."""
    replay_dir = tmp_path
    template_name = "existing.json"
    expected = os.path.join(str(replay_dir), "existing.json")
    result = get_file_name(replay_dir, template_name)
    assert result == expected, f"Expected {expected!r}, got {result!r}"

def test_get_file_name_with_path_object(tmp_path: Path):
    """Passing a Path object as replay_dir works correctly."""
    replay_dir = Path(tmp_path)
    template_name = "path_test"
    expected = os.path.join(str(replay_dir), "path_test.json")
    result = get_file_name(replay_dir, template_name)
    assert result == expected, f"Expected {expected!r}, got {result!r}"

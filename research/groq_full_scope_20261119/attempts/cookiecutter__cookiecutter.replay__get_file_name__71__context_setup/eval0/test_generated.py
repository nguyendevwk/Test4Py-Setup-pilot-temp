import os
import json
import pytest
from pathlib import Path
from cookiecutter.replay import get_file_name

def test_get_file_name_adds_suffix(tmp_path: Path):
    """When template name has no .json suffix, one is added."""
    replay_dir = tmp_path
    template_name = "my_template"
    expected = os.path.join(str(replay_dir), "my_template.json")
    result = get_file_name(replay_dir, template_name)
    assert result == expected
    assert result.endswith(".json")

def test_get_file_name_no_suffix_added(tmp_path: Path):
    """When template name already ends with .json, no extra suffix is added."""
    replay_dir = tmp_path
    template_name = "existing.json"
    expected = os.path.join(str(replay_dir), "existing.json")
    result = get_file_name(replay_dir, template_name)
    assert result == expected
    assert result.endswith(".json")

def test_get_file_name_accepts_path_object(tmp_path: Path):
    """The function accepts a pathlib.Path object for replay_dir."""
    replay_dir = Path(tmp_path)
    template_name = "sample"
    result = get_file_name(replay_dir, template_name)
    # result should be a string path
    assert isinstance(result, str)
    # The path should resolve to the expected file
    expected = os.path.join(str(tmp_path), "sample.json")
    assert result == expected

import json
import os
import pytest
from pathlib import Path

from cookiecutter.replay import load, get_file_name


def test_load_normal(tmp_path: Path):
    """Test that load returns the JSON content when the file is valid."""
    # Arrange: create a valid replay file
    data = {"cookiecutter": {"name": "example"}, "other": 123}
    file_path = tmp_path / "replay.json"
    file_path.write_text(json.dumps(data), encoding="utf-8")

    # Act: load the file
    result = load(tmp_path, "replay.json")

    # Assert: the returned dict matches the original data
    assert result == data
    assert "cookiecutter" in result
    assert result["cookiecutter"]["name"] == "example"


def test_load_missing_cookiecutter(tmp_path: Path):
    """Test that load raises ValueError when 'cookiecutter' key is missing."""
    # Arrange: create a replay file without the required key
    data = {"not_cookiecutter": {"name": "example"}}
    file_path = tmp_path / "missing.json"
    file_path.write_text(json.dumps(data), encoding="utf-8")

    # Act & Assert: loading should raise ValueError
    with pytest.raises(ValueError, match="Context is required to contain a cookiecutter key"):
        load(tmp_path, "missing.json")


def test_get_file_name_with_suffix(tmp_path: Path):
    """Test that get_file_name correctly appends .json when missing."""
    # Arrange: template name without extension
    template_name = "template"
    expected = os.path.join(tmp_path, "template.json")

    # Act: compute file name
    result = get_file_name(tmp_path, template_name)

    # Assert: the result matches the expected path
    assert result == expected

    # Also test when the template name already ends with .json
    template_name_json = "template.json"
    expected_json = os.path.join(tmp_path, "template.json")
    assert get_file_name(tmp_path, template_name_json) == expected_json

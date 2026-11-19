import os
import json
import pytest
from cookiecutter.repository import repository_has_cookiecutter_json

def test_repository_has_cookiecutter_json_true(tmp_path):
    """When the directory exists and contains cookiecutter.json, the function returns True."""
    # Create a temporary directory and a cookiecutter.json file inside it
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    json_path = repo_dir / "cookiecutter.json"
    json_path.write_text(json.dumps({"name": "test"}))
    # Assert that the function detects the file
    assert repository_has_cookiecutter_json(str(repo_dir)) is True

def test_repository_has_cookiecutter_json_false_no_file(tmp_path):
    """When the directory exists but does not contain cookiecutter.json, the function returns False."""
    # Create a temporary directory without cookiecutter.json
    repo_dir = tmp_path / "empty_repo"
    repo_dir.mkdir()
    # Assert that the function returns False
    assert repository_has_cookiecutter_json(str(repo_dir)) is False

def test_repository_has_cookiecutter_json_false_no_dir(tmp_path):
    """When the directory does not exist, the function returns False."""
    # Define a path that does not exist
    non_existent_dir = tmp_path / "nonexistent"
    # Assert that the function returns False
    assert repository_has_cookiecutter_json(str(non_existent_dir)) is False

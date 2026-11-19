import os
import json
import pytest
from cookiecutter.repository import repository_has_cookiecutter_json

def test_repository_has_cookiecutter_json_true(tmp_path):
    """When a directory contains a cookiecutter.json file, the function returns True."""
    # Create a temporary directory and a cookiecutter.json file inside it
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    json_path = repo_dir / "cookiecutter.json"
    json_path.write_text(json.dumps({"name": "test"}))
    # Assert that the function detects the file
    assert repository_has_cookiecutter_json(str(repo_dir)) is True

def test_repository_has_cookiecutter_json_false_missing_file(tmp_path):
    """When the directory exists but lacks cookiecutter.json, the function returns False."""
    # Create a temporary directory without the JSON file
    repo_dir = tmp_path / "empty_repo"
    repo_dir.mkdir()
    # Assert that the function returns False
    assert repository_has_cookiecutter_json(str(repo_dir)) is False

def test_repository_has_cookiecutter_json_false_nonexistent(tmp_path):
    """When the path does not exist, the function returns False."""
    # Define a path that does not exist
    nonexistent_path = tmp_path / "does_not_exist"
    # Assert that the function returns False
    assert repository_has_cookiecutter_json(str(nonexistent_path)) is False

import os
import json
import tempfile
import pytest
from cookiecutter.repository import repository_has_cookiecutter_json

def test_repository_has_cookiecutter_json_true(tmp_path):
    """When the directory exists and contains cookiecutter.json, the function returns True."""
    # Create a temporary directory and a cookiecutter.json file inside it
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    json_path = repo_dir / "cookiecutter.json"
    json_path.write_text(json.dumps({"name": "test"}))
    # Verify that the function detects the file
    assert repository_has_cookiecutter_json(str(repo_dir)) is True

def test_repository_has_cookiecutter_json_false_no_file(tmp_path):
    """When the directory exists but does not contain cookiecutter.json, the function returns False."""
    # Create a temporary directory without the required file
    repo_dir = tmp_path / "empty_repo"
    repo_dir.mkdir()
    # Verify that the function correctly returns False
    assert repository_has_cookiecutter_json(str(repo_dir)) is False

def test_repository_has_cookiecutter_json_false_nonexistent(tmp_path):
    """When the directory does not exist, the function returns False."""
    # Define a path that does not exist
    nonexistent_dir = tmp_path / "nonexistent"
    # Verify that the function correctly returns False for a missing directory
    assert repository_has_cookiecutter_json(str(nonexistent_dir)) is False

import os
import json
import tempfile
import pytest
from cookiecutter.repository import repository_has_cookiecutter_json

def test_repository_has_cookiecutter_json_true(tmp_path):
    """When a directory contains cookiecutter.json, the function returns True."""
    # Create a temporary directory that will act as the repository
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    # Create a cookiecutter.json file inside it
    json_path = repo_dir / "cookiecutter.json"
    json_path.write_text(json.dumps({"name": "test"}))
    # Verify that the function detects the file
    assert repository_has_cookiecutter_json(str(repo_dir)) is True

def test_repository_has_cookiecutter_json_false_missing_file(tmp_path):
    """When a directory exists but lacks cookiecutter.json, the function returns False."""
    # Create a temporary directory without the required file
    repo_dir = tmp_path / "empty_repo"
    repo_dir.mkdir()
    # Ensure the file does not exist
    assert not (repo_dir / "cookiecutter.json").exists()
    # Verify that the function returns False
    assert repository_has_cookiecutter_json(str(repo_dir)) is False

def test_repository_has_cookiecutter_json_false_not_a_directory(tmp_path):
    """When the path exists but is not a directory, the function returns False."""
    # Create a temporary file instead of a directory
    file_path = tmp_path / "not_a_dir"
    file_path.write_text("just a file")
    # Verify that the function returns False for a file path
    assert repository_has_cookiecutter_json(str(file_path)) is False

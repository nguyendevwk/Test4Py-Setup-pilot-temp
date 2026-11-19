import os
import pytest
from cookiecutter.repository import repository_has_cookiecutter_json

def test_repository_has_cookiecutter_json_true(tmp_path):
    # Create a temporary directory that will act as a repository
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    # Place a cookiecutter.json file inside it
    (repo_dir / "cookiecutter.json").write_text('{"name": "test"}')
    # The function should return True
    assert repository_has_cookiecutter_json(str(repo_dir)) is True

def test_repository_has_cookiecutter_json_false_missing_file(tmp_path):
    # Create a temporary directory without cookiecutter.json
    repo_dir = tmp_path / "repo_no_file"
    repo_dir.mkdir()
    # The function should return False because the file is missing
    assert repository_has_cookiecutter_json(str(repo_dir)) is False

def test_repository_has_cookiecutter_json_false_missing_dir(tmp_path):
    # Provide a path that does not exist
    non_existent_dir = tmp_path / "nonexistent"
    # The function should return False because the directory does not exist
    assert repository_has_cookiecutter_json(str(non_existent_dir)) is False

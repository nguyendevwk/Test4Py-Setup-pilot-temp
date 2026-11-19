import os
import pytest
from cookiecutter.repository import repository_has_cookiecutter_json

def test_repository_has_cookiecutter_json_true(tmp_path):
    # Create a temporary directory that contains a cookiecutter.json file
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    (repo_dir / "cookiecutter.json").write_text('{"name": "test"}')
    # The function should return True
    assert repository_has_cookiecutter_json(str(repo_dir)) is True

def test_repository_has_cookiecutter_json_false_missing_file(tmp_path):
    # Create a temporary directory without cookiecutter.json
    repo_dir = tmp_path / "empty_repo"
    repo_dir.mkdir()
    # The function should return False because the file is missing
    assert repository_has_cookiecutter_json(str(repo_dir)) is False

def test_repository_has_cookiecutter_json_false_nonexistent(tmp_path):
    # Provide a path that does not exist
    nonexistent_dir = tmp_path / "does_not_exist"
    # The function should return False because the directory does not exist
    assert repository_has_cookiecutter_json(str(nonexistent_dir)) is False

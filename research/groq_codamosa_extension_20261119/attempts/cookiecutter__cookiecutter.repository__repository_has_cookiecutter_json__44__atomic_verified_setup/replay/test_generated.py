import os
import pytest
from cookiecutter.repository import repository_has_cookiecutter_json

def test_repository_has_cookiecutter_json_true(tmp_path):
    # Create a temporary directory that mimics a repository
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    # Place a cookiecutter.json file inside
    (repo_dir / "cookiecutter.json").write_text('{"name": "test"}')
    # The function should return True
    assert repository_has_cookiecutter_json(str(repo_dir)) is True

def test_repository_has_cookiecutter_json_false_missing_file(tmp_path):
    # Create a temporary directory without cookiecutter.json
    repo_dir = tmp_path / "repo_no_json"
    repo_dir.mkdir()
    # The function should return False because the file is missing
    assert repository_has_cookiecutter_json(str(repo_dir)) is False

def test_repository_has_cookiecutter_json_false_not_a_directory(tmp_path):
    # Create a file instead of a directory
    file_path = tmp_path / "not_a_dir"
    file_path.write_text("just a file")
    # The function should return False because the path is not a directory
    assert repository_has_cookiecutter_json(str(file_path)) is False

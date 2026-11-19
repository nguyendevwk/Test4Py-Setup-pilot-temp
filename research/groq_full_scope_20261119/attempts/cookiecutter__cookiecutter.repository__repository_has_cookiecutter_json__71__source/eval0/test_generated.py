import os
import pytest
from cookiecutter.repository import repository_has_cookiecutter_json

def test_repository_has_cookiecutter_json_true(tmp_path):
    # Create a temporary directory and a cookiecutter.json file inside it
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    (repo_dir / "cookiecutter.json").write_text('{"name": "test"}')
    # The function should return True when both the directory and file exist
    assert repository_has_cookiecutter_json(str(repo_dir)) is True

def test_repository_has_cookiecutter_json_false_no_file(tmp_path):
    # Create a temporary directory without the cookiecutter.json file
    repo_dir = tmp_path / "empty_repo"
    repo_dir.mkdir()
    # The function should return False because the file is missing
    assert repository_has_cookiecutter_json(str(repo_dir)) is False

def test_repository_has_cookiecutter_json_false_no_directory(tmp_path):
    # Provide a path that does not exist
    non_existent_dir = tmp_path / "nonexistent"
    # The function should return False when the directory does not exist
    assert repository_has_cookiecutter_json(str(non_existent_dir)) is False

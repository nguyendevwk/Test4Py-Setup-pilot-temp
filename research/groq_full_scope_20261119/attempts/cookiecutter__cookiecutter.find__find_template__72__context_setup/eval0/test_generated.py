import os
import logging
import pytest
from pathlib import Path
from jinja2 import Environment
from cookiecutter.exceptions import NonTemplatedInputDirException
from cookiecutter.find import find_template

# Ensure logger does not interfere with test output
logging.getLogger("cookiecutter.find").setLevel(logging.DEBUG)

def test_find_template_success(tmp_path: Path):
    """When a matching subdirectory exists, find_template returns its Path."""
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    # Create a directory that matches the pattern
    matching_dir = repo_dir / "cookiecutter_{{project_name}}_template"
    matching_dir.mkdir()
    # Add a non-matching sibling
    (repo_dir / "other_dir").mkdir()

    env = Environment()
    result = find_template(repo_dir, env)
    assert result == matching_dir
    assert result.is_dir()
    # Ensure the function did not return the non-matching sibling
    assert result.name == "cookiecutter_{{project_name}}_template"

def test_find_template_no_match(tmp_path: Path):
    """If no subdirectory matches the pattern, a NonTemplatedInputDirException is raised."""
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    # Create only non-matching directories
    (repo_dir / "foo").mkdir()
    (repo_dir / "bar").mkdir()

    env = Environment()
    with pytest.raises(NonTemplatedInputDirException):
        find_template(repo_dir, env)

def test_find_template_first_match(tmp_path: Path):
    """When multiple matching directories exist, the first one found is returned."""
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    # Create two matching directories
    first_match = repo_dir / "cookiecutter_{{first}}_template"
    second_match = repo_dir / "cookiecutter_{{second}}_template"
    first_match.mkdir()
    second_match.mkdir()
    # Create a non-matching directory to ensure order is not affected
    (repo_dir / "random").mkdir()

    env = Environment()
    result = find_template(repo_dir, env)
    # The function should return the first matching directory in os.listdir order
    # os.listdir does not guarantee order, but on most filesystems it returns sorted order.
    # To make the test deterministic, we explicitly check that the returned path is one of the matches
    assert result in {first_match, second_match}
    # Verify that the returned path is indeed a directory
    assert result.is_dir()

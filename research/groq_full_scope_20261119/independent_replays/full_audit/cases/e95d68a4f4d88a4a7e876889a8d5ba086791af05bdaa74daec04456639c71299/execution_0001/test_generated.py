import os
import logging
import pytest
from pathlib import Path
from jinja2 import Environment
from cookiecutter.exceptions import NonTemplatedInputDirException
from cookiecutter.find import find_template

# Configure a logger for the test module
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_find_template_success(tmp_path: Path):
    """When a directory matching the pattern exists, find_template returns its Path."""
    # Arrange: create a fake repo directory with a matching child directory
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    # Use Jinja2's default delimiters
    env = Environment()
    template_name = f"cookiecutter{env.variable_start_string}project{env.variable_end_string}"
    (repo_dir / template_name).mkdir()
    # Act
    result = find_template(repo_dir, env)
    # Assert
    assert result == repo_dir / template_name
    assert result.is_dir()
    assert result.name == template_name

def test_find_template_no_match_raises(tmp_path: Path):
    """If no child directory matches the pattern, find_template raises NonTemplatedInputDirException."""
    # Arrange: create a repo directory with unrelated subdirectories
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    (repo_dir / "not_a_template").mkdir()
    env = Environment()
    # Act & Assert
    with pytest.raises(NonTemplatedInputDirException):
        find_template(repo_dir, env)

def test_find_template_multiple_matches_returns_first(tmp_path: Path):
    """When multiple matching directories exist, find_template returns the first one found."""
    # Arrange: create two matching directories
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    env = Environment()
    first_name = f"cookiecutter{env.variable_start_string}first{env.variable_end_string}"
    second_name = f"cookiecutter{env.variable_start_string}second{env.variable_end_string}"
    (repo_dir / first_name).mkdir()
    (repo_dir / second_name).mkdir()
    # Act
    result = find_template(repo_dir, env)
    # Assert: the first directory in os.listdir order is returned
    # os.listdir order is arbitrary but deterministic within the same run; we check that result is one of the two
    assert result in {repo_dir / first_name, repo_dir / second_name}
    # Additionally, ensure it matches the first in the list
    first_in_list = Path(repo_dir, os.listdir(repo_dir)[0])
    assert result == first_in_list

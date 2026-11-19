import os
from pathlib import Path

import pytest
from jinja2 import Environment
from cookiecutter.exceptions import NonTemplatedInputDirException

from cookiecutter.find import find_template


def test_find_template_returns_correct_path(tmp_path: Path):
    """When a matching subdirectory exists, the function returns its Path."""
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    # Create a directory that matches the pattern
    matching_dir = repo_dir / "cookiecutter_{{project_name}}_template"
    matching_dir.mkdir()
    # Create another unrelated directory
    (repo_dir / "other_dir").mkdir()

    env = Environment()
    result = find_template(repo_dir, env)
    assert result == matching_dir
    assert result.is_dir()


def test_find_template_selects_first_match(tmp_path: Path):
    """If multiple matching directories exist, the first one in os.listdir order is chosen."""
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    # Two matching directories; order depends on os.listdir
    first = repo_dir / "cookiecutter_{{first}}_template"
    second = repo_dir / "cookiecutter_{{second}}_template"
    first.mkdir()
    second.mkdir()

    env = Environment()
    result = find_template(repo_dir, env)
    # os.listdir may return in arbitrary order; we assert that the result is one of the two
    assert result in {first, second}
    assert result.is_dir()


def test_find_template_raises_on_no_match(tmp_path: Path):
    """If no directory matches the pattern, a NonTemplatedInputDirException is raised."""
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    # Create directories that do not match the pattern
    (repo_dir / "not_a_template").mkdir()
    (repo_dir / "cookiecutter_no_braces").mkdir()

    env = Environment()
    with pytest.raises(NonTemplatedInputDirException):
        find_template(repo_dir, env)

import os
from pathlib import Path

import pytest
from jinja2 import Environment
from cookiecutter.exceptions import NonTemplatedInputDirException

from cookiecutter.find import find_template


def test_find_template_normal(tmp_path: Path) -> None:
    """When a matching subdirectory exists, the function returns its Path."""
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    # Create a directory that matches the pattern
    template_dir = repo_dir / "cookiecutter_{{project_name}}_template"
    template_dir.mkdir()
    # Create another unrelated directory
    (repo_dir / "other").mkdir()

    env = Environment()
    result = find_template(repo_dir, env)
    assert result == template_dir
    assert result.is_dir()


def test_find_template_boundary(tmp_path: Path) -> None:
    """If multiple matching directories exist, the first one in os.listdir order is returned."""
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    # Create two matching directories
    first = repo_dir / "cookiecutter_{{first}}_template"
    second = repo_dir / "cookiecutter_{{second}}_template"
    first.mkdir()
    second.mkdir()

    env = Environment()
    result = find_template(repo_dir, env)
    # os.listdir may not guarantee order, but the function returns the first match it encounters
    assert result in {first, second}
    assert result.is_dir()


def test_find_template_error(tmp_path: Path) -> None:
    """If no matching subdirectory exists, a NonTemplatedInputDirException is raised."""
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    # Create a non-matching directory
    (repo_dir / "not_a_template").mkdir()

    env = Environment()
    with pytest.raises(NonTemplatedInputDirException):
        find_template(repo_dir, env)

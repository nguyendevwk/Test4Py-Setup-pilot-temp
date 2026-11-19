import os
from pathlib import Path
import pytest
from jinja2 import Environment
from cookiecutter.exceptions import NonTemplatedInputDirException
from cookiecutter.find import find_template

@pytest.fixture
def env() -> Environment:
    """Provide a Jinja2 Environment with default delimiters."""
    return Environment()

def test_find_template_success(tmp_path: Path, env: Environment) -> None:
    """
    Verify that find_template correctly identifies a child directory
    whose name contains the Jinja2 delimiters and the string 'cookiecutter'.
    """
    # Create a matching directory
    matching_dir = tmp_path / "cookiecutter_{{project_name}}_template"
    matching_dir.mkdir()
    # Create a non-matching sibling
    (tmp_path / "not_a_template").mkdir()

    result = find_template(tmp_path, env)
    assert result == matching_dir, "Returned path should be the matching directory"

def test_find_template_no_match(tmp_path: Path, env: Environment) -> None:
    """
    Verify that find_template raises NonTemplatedInputDirException when
    no suitable child directory exists.
    """
    # Create only non-matching directories
    (tmp_path / "random_dir").mkdir()
    (tmp_path / "another_dir").mkdir()

    with pytest.raises(NonTemplatedInputDirException):
        find_template(tmp_path, env)

def test_find_template_multiple_matches(tmp_path: Path, env: Environment) -> None:
    """
    Verify that find_template returns the first matching directory
    when multiple candidates exist.
    """
    # Create two matching directories
    first_match = tmp_path / "cookiecutter_{{first}}_template"
    second_match = tmp_path / "cookiecutter_{{second}}_template"
    first_match.mkdir()
    second_match.mkdir()

    result = find_template(tmp_path, env)
    assert result == first_match, "Should return the first matching directory found"

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
    Verify that find_template returns the correct Path when a matching
    directory exists. The directory name must contain 'cookiecutter' and
    the Jinja2 variable delimiters.
    """
    # Create a matching directory
    matching_dir = tmp_path / "my_cookiecutter_{{project_name}}_template"
    matching_dir.mkdir()
    # Create a non-matching sibling
    (tmp_path / "other_dir").mkdir()

    result = find_template(tmp_path, env)

    assert isinstance(result, Path), "Result should be a Path instance"
    assert result == matching_dir, "Returned path should match the template directory"
    assert result.is_dir(), "Returned path should be an existing directory"

def test_find_template_no_match(tmp_path: Path, env: Environment) -> None:
    """
    Verify that find_template raises NonTemplatedInputDirException when no
    directory matches the required pattern.
    """
    # Create a directory that does not match the pattern
    (tmp_path / "plain_dir").mkdir()

    with pytest.raises(NonTemplatedInputDirException):
        find_template(tmp_path, env)

def test_find_template_multiple_matches(tmp_path: Path, env: Environment) -> None:
    """
    Verify that find_template returns the first matching directory when
    multiple candidates exist. The function should not raise an exception
    and should return the first match in the os.listdir order.
    """
    # Create two matching directories
    first_match = tmp_path / "first_cookiecutter_{{name}}_template"
    second_match = tmp_path / "second_cookiecutter_{{name}}_template"
    first_match.mkdir()
    second_match.mkdir()

    # Ensure os.listdir order is deterministic by sorting the names
    # (os.listdir may not guarantee order, but on most systems it is sorted)
    result = find_template(tmp_path, env)

    assert result == first_match, (
        "find_template should return the first matching directory in the list"
    )
    assert result.is_dir(), "Returned path should be an existing directory"

import os
import zipfile
import pathlib
import pytest
from cookiecutter.repository import determine_repo_dir, RepositoryNotFound


def test_determine_repo_dir_local_path(tmp_path):
    """When a local directory containing cookiecutter.json is supplied,
    the function should return that directory and not schedule cleanup."""
    # Create a fake template directory with cookiecutter.json
    template_dir = tmp_path / "my_template"
    template_dir.mkdir()
    (template_dir / "cookiecutter.json").write_text('{"foo":"bar"}')

    repo_dir, cleanup = determine_repo_dir(
        template=str(template_dir),
        abbreviations={},
        clone_to_dir=tmp_path,
        checkout=None,
        no_input=True,
        password=None,
        directory=None,
    )

    assert repo_dir == str(template_dir)
    assert cleanup is False
    assert os.path.isdir(repo_dir)
    assert os.path.isfile(os.path.join(repo_dir, "cookiecutter.json"))


def test_determine_repo_dir_zip_file(tmp_path):
    """When a zip file containing cookiecutter.json is supplied,
    the function should unzip it, return the extracted directory,
    and indicate that cleanup is required."""
    # Create a zip file with cookiecutter.json
    zip_path = tmp_path / "template.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("cookiecutter.json", '{"foo":"bar"}')

    repo_dir, cleanup = determine_repo_dir(
        template=str(zip_path),
        abbreviations={},
        clone_to_dir=tmp_path,
        checkout=None,
        no_input=True,
        password=None,
        directory=None,
    )

    # The extracted directory should be inside tmp_path
    assert repo_dir.startswith(str(tmp_path))
    assert cleanup is True
    assert os.path.isdir(repo_dir)
    assert os.path.isfile(os.path.join(repo_dir, "cookiecutter.json"))


def test_determine_repo_dir_abbreviation_and_error(tmp_path):
    """Abbreviations should be expanded, and an error should be raised
    if no valid repository is found."""
    # Define an abbreviation that expands to a non‑existent path
    abbreviations = {"foo": "nonexistent/path"}

    with pytest.raises(RepositoryNotFound) as excinfo:
        determine_repo_dir(
            template="foo",
            abbreviations=abbreviations,
            clone_to_dir=tmp_path,
            checkout=None,
            no_input=True,
            password=None,
            directory=None,
        )

    # The exception message should mention the expanded path
    assert "nonexistent/path" in str(excinfo.value)

import os
import zipfile
import pathlib
import pytest
from cookiecutter.repository import determine_repo_dir
from cookiecutter.exceptions import RepositoryNotFound

@pytest.fixture
def tmp_repo(tmp_path):
    """Create a temporary directory that contains a cookiecutter.json file."""
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    (repo_dir / "cookiecutter.json").write_text('{"project_name": "test"}')
    return repo_dir

def test_determine_repo_dir_with_local_path(tmp_repo, tmp_path):
    """When the template is a local path, the function returns that path."""
    clone_to_dir = tmp_path / "clone"
    clone_to_dir.mkdir()
    result_dir, cleanup = determine_repo_dir(
        template=str(tmp_repo),
        abbreviations={},
        clone_to_dir=clone_to_dir,
        checkout=None,
        no_input=True,
        password=None,
        directory=None,
    )
    assert result_dir == str(tmp_repo)
    assert cleanup is False

def test_determine_repo_dir_with_zip_file(tmp_path):
    """When the template is a zip file, the function unzips it and returns the dir."""
    # Create a zip file containing a cookiecutter.json
    zip_path = tmp_path / "template.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("cookiecutter.json", '{"project_name": "zip"}')
    clone_to_dir = tmp_path / "clone"
    clone_to_dir.mkdir()
    result_dir, cleanup = determine_repo_dir(
        template=str(zip_path),
        abbreviations={},
        clone_to_dir=clone_to_dir,
        checkout=None,
        no_input=True,
        password=None,
        directory=None,
    )
    # The unzipped directory should be inside clone_to_dir
    assert result_dir.startswith(str(clone_to_dir))
    assert os.path.isfile(os.path.join(result_dir, "cookiecutter.json"))
    assert cleanup is True

def test_determine_repo_dir_missing_cookiecutter(tmp_path):
    """If no cookiecutter.json is found, RepositoryNotFound is raised."""
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    clone_to_dir = tmp_path / "clone"
    clone_to_dir.mkdir()
    with pytest.raises(RepositoryNotFound) as excinfo:
        determine_repo_dir(
            template=str(empty_dir),
            abbreviations={},
            clone_to_dir=clone_to_dir,
            checkout=None,
            no_input=True,
            password=None,
            directory=None,
        )
    assert str(empty_dir) in str(excinfo.value)

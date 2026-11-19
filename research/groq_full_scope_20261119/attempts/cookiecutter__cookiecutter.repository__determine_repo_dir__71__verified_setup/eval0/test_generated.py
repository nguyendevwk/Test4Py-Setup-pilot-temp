import os
import zipfile
import shutil
from pathlib import Path
import pytest
from cookiecutter.repository import determine_repo_dir
from cookiecutter.exceptions import RepositoryNotFound

def test_determine_repo_dir_local(tmp_path):
    # Create a local template directory with cookiecutter.json
    template_dir = tmp_path / "my_template"
    template_dir.mkdir()
    (template_dir / "cookiecutter.json").write_text('{"project_name":"test"}')
    # Call determine_repo_dir with the local path
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

def test_determine_repo_dir_zip(tmp_path):
    # Create a zip file containing cookiecutter.json
    zip_path = tmp_path / "template.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("cookiecutter.json", '{"project_name":"zip"}')
    # Call determine_repo_dir with the zip file path
    repo_dir, cleanup = determine_repo_dir(
        template=str(zip_path),
        abbreviations={},
        clone_to_dir=tmp_path,
        checkout=None,
        no_input=True,
        password=None,
        directory=None,
    )
    # The zip should be extracted into a temporary directory
    assert Path(repo_dir).is_dir()
    assert (Path(repo_dir) / "cookiecutter.json").exists()
    assert cleanup is True

def test_determine_repo_dir_not_found(tmp_path):
    # Provide a non-existent path
    non_existent = tmp_path / "does_not_exist"
    with pytest.raises(RepositoryNotFound) as excinfo:
        determine_repo_dir(
            template=str(non_existent),
            abbreviations={},
            clone_to_dir=tmp_path,
            checkout=None,
            no_input=True,
            password=None,
            directory=None,
        )
    assert str(non_existent) in str(excinfo.value)

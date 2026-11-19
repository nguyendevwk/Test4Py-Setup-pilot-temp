import os
import zipfile
import pathlib
import pytest
from cookiecutter.repository import determine_repo_dir, RepositoryNotFound

# Helper to create a minimal cookiecutter template directory
def make_template_dir(tmp_path: pathlib.Path, name: str) -> pathlib.Path:
    dir_path = tmp_path / name
    dir_path.mkdir()
    (dir_path / "cookiecutter.json").write_text('{"foo":"bar"}')
    return dir_path

# Helper to create a zip file containing a cookiecutter template
def make_template_zip(tmp_path: pathlib.Path, name: str) -> pathlib.Path:
    dir_path = make_template_dir(tmp_path, name)
    zip_path = tmp_path / f"{name}.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        for root, _, files in os.walk(dir_path):
            for f in files:
                full_path = pathlib.Path(root) / f
                zf.write(full_path, arcname=str(full_path.relative_to(dir_path.parent)))
    return zip_path

def test_determine_repo_dir_local_path(tmp_path: pathlib.Path):
    # Create a local template directory
    template_dir = make_template_dir(tmp_path, "mytemplate")
    # Call determine_repo_dir with the local path
    result_dir, cleanup = determine_repo_dir(
        template=str(template_dir),
        abbreviations={},
        clone_to_dir=tmp_path,
        checkout=None,
        no_input=True,
        password=None,
        directory=None,
    )
    # The returned directory should be the same as the created one
    assert pathlib.Path(result_dir) == template_dir
    # No cleanup should be requested for a local path
    assert cleanup is False

def test_determine_repo_dir_zip_file(tmp_path: pathlib.Path):
    # Create a zip file containing a template
    zip_path = make_template_zip(tmp_path, "ziptemplate")
    # Call determine_repo_dir with the zip file path
    result_dir, cleanup = determine_repo_dir(
        template=str(zip_path),
        abbreviations={},
        clone_to_dir=tmp_path,
        checkout=None,
        no_input=True,
        password=None,
        directory=None,
    )
    # The returned directory should be inside tmp_path and contain cookiecutter.json
    assert pathlib.Path(result_dir).is_dir()
    assert (pathlib.Path(result_dir) / "cookiecutter.json").exists()
    # Cleanup should be True for a zip extraction
    assert cleanup is True

def test_determine_repo_dir_not_found(tmp_path: pathlib.Path):
    # Provide a non-existent template path
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
    # The exception message should mention the template path
    assert str(non_existent) in str(excinfo.value)
